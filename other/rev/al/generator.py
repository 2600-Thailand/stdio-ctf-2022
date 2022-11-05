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
        x = self.relu(x)
        x = torch.abs(self.threshold(-x))
        x = self.hidden_layer(x)
        x = self.threshold2(x)
        x = x + (0.01 * s) # weighted skip connection
        x = self.output_layer(x)
        return x

model = StorageAuthModel()
model.eval()

# generate weight from flag
@torch.no_grad()
def init_weights(m):
    global x
    # input layer
    if type(m) == nn.Linear and len(m.weight) == 82:
        #m.bias.fill_(0)
        for i in range(0,41):
            m.bias[i] = -(x[i]-1)
            for j in range(41):
                m.weight[i][j] = 1 if i == j else 0
    # hidden layer
    if type(m) == nn.Linear and len(m.weight) == 82 and len(m.weight[0]) == 82:
        m.bias[0] = 0
        m.weight[0] = torch.cat((torch.ones(41),torch.zeros(41)))
    # output layer
    if type(m) == nn.Linear and len(m.weight) == 10 and len(m.weight[0]) == 82:
        m.bias[0] = 0
        m.weight[0] = torch.cat((torch.ones(1)/41,torch.zeros(81)))
model.apply(init_weights)

torch.save(model.state_dict(), 'bankde-secret')
print("bankde-secret created")

# test
print("== validating the flag with generated file")

import subprocess
import secrets
invalid = "STDIO99{17adbcf543e851aa9216acc9d7206b96}"
invalid2 = "STDIO11{17adbcf543e851aa9216acc9d7206b96}"

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
assert out, "Something went wrong"
print(out)

print("testing with secret:",invalid2)
po = subprocess.Popen(['python','app.py'],stdin=subprocess.PIPE ,stdout=subprocess.PIPE, text=True)
po.stdin.write(invalid2 + '\n')
po.stdin.flush()
out = po.stdout.read()
assert out, "Something went wrong"
print(out)

# zip
print("== compressing final chal")
import zipfile
with zipfile.ZipFile(chal_zip_filename, mode="w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
    archive.write("app.py")
    archive.write("bankde-secret")
print("created", chal_zip_filename)
