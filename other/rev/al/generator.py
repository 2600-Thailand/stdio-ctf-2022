#AL chal generator
flag = "STDIO11{3c5c3184f6cdac4263b73791c5a95d24}"
chal_zip_filename = "al.zip"

import os

print("== creating app.py")
os.system("cp app.template.py app.py")
print("app.py created")

print("== creating bankde-secret weight")
import torch
import torch.nn as nn
torch.manual_seed(1337)

# flag to tensor
x = torch.tensor(bytearray(flag.encode()),dtype=torch.float32)

class StorageAuthModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.input_layer  = nn.Linear(41, 82)
        self.relu         = nn.ReLU()
        self.threshold    = nn.Threshold(-1.0001, 0)
        self.hidden_layer = nn.Linear(82,82)
        self.threshold2   = nn.Threshold(40, 0)
        self.output_layer = nn.Linear(82, 10)

    def forward(self, x):
        x = self.input_layer(x) 
        s = torch.cat((torch.zeros(1), x[41:], x[41:-1]))
        x = self.relu(x) # y = max(x,0) to remove all negative values
        x = torch.abs(self.threshold(-x)) # to change all non 1 values to 0
        x = self.hidden_layer(x)
        x = self.threshold2(x) # to verify whether the node is 41, otherwise set to 0
        x = x + (0.01 * s) # weighted skip connection, to add some noise we don't care
        x = self.output_layer(x)
        # e.g. [ 0.0000, -0.1865, -0.1444, -0.2091,  0.0968, -0.3612,  0.3356, -0.4497, -0.0750, -0.0009]
        return x

model = StorageAuthModel()
model.eval()

# generate weight from flag
# ======================================================================================
@torch.no_grad()
def init_weights(m):
    global x # = flag
    # input layer (41) --> (82)
    if type(m) == nn.Linear and len(m.weight) == 82:
        # the first layer is normal linear NN (y = weight * x + bias)
        # for the first half of first hidden layer's weight,
        for i in range(0,41):
            # we fix the hidden node's bias to -(ord(flag[i]) -1)
            m.bias[i] = -(x[i]-1) 
            # and we fix the weight for each nodes to be 1-to-1
            for j in range(41):
                m.weight[i][j] = 1 if i == j else 0
            # means that the first have of hidden layer will equal to correct_flag - 1
            # eg. if the first flag is 'S' the first input layer's output will be 1

    # then we will perform activation function with ReLU (y = max(x,0)) to remove all negative values
    # after that to handle all non "1" value, we will multiply the neurons with -1 and do the same thing to remove all
    # so the output of first 41 hidden layer will be only 0 if the flag[i] is incorrect and 1 if the flag[i] is correct 

    # hidden layer
    if type(m) == nn.Linear and len(m.weight) == 82 and len(m.weight[0]) == 82:
        # the second layer is also normal linear NN (y = weight * x + bias)
        # we set bias of the "first" node to be 0
        m.bias[0] = 0
        # we set weight of the "first" node to be calculated only from first 41 output (which is previous 0 and 1)
        m.weight[0] = torch.cat((torch.ones(41),torch.zeros(41)))
        # after this we will have skip connection in "forward" pass to add input value to other hidden nodes
        # but we don't care since they are all noise, we only use first 41 nodes for the calculations (which is anlready
        # done on the first layer

    # output layer
    if type(m) == nn.Linear and len(m.weight) == 10 and len(m.weight[0]) == 82:
        m.bias[0] = 0 # no need bias for the first output
        # this layer will sum all first 41 node's values (0 if not the flag, 1 if the character similar to flag)
        # to be in range of [0,41]
        # setting first output node's weight to use only the first output of hidden node, and disregard the rest 81 nodes
        
        # there is "threshold2" activation function to validate whether the result is > 40 or not (fill the flag correctlly)
        # otherwise the output value is 0, this will make the first node's output to be either 0 or 41
        m.weight[0] = torch.cat((torch.ones(1)/41,torch.zeros(81)))
        # then the output will be like [0 or 1(from 41/41), and other 8 noise from randomized weight which we don't care]
        # this is also normal linear NN (y = (1/41) * x + 0) for the first node
model.apply(init_weights)
# ======================================================================================

torch.save(model.state_dict(), 'bankde-secret')
print("bankde-secret created")

# test
print("== validating the flag with generated file")

import subprocess
import secrets
invalid = "STDIO99{17adbcf543e851aa9216acc9d7206b96}"

print("testing with secret:",flag)
po = subprocess.Popen(['python','app.py'],stdin=subprocess.PIPE ,stdout=subprocess.PIPE, text=True)
po.stdin.write(flag + '\n')
po.stdin.flush()
out = po.stdout.read()
assert "Correct!" in out, "Something went wrong"
print(out)

print("testing with secret:",invalid)
po = subprocess.Popen(['python','app.py'],stdin=subprocess.PIPE ,stdout=subprocess.PIPE, text=True)
po.stdin.write(invalid + '\n')
po.stdin.flush()
out = po.stdout.read()
assert "Incorrect secret" in out, "Something went wrong"
print(out)

# zip
print("== compressing final chal")
import zipfile
with zipfile.ZipFile(chal_zip_filename, mode="w") as archive:
    archive.write("app.py")
    archive.write("bankde-secret")
print("created", chal_zip_filename)

# generated https://gitlab.com/stdio-ctf/stdio-ctf-2022/-/raw/main/file/ch11_rev_AL.zip?inline=false
