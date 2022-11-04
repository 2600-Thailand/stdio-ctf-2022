import torch
import torch.nn as nn
import re

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

# initialize neuron network model
auth = StorageAuthModel()
secret = torch.load('bankde-secret')
auth.eval()
auth.load_state_dict(secret)


print("Welcome to AI-protected secret storage")
secret = input("Enter secret: ")
assert len(secret) == 41, "Invalid secret format length"
assert re.search("STDIO11{[0-9a-f]{32}\}", secret), "Invalid secret format"

password_tensor = torch.tensor(bytearray(secret.encode()), dtype=torch.float32)
ans = auth(password_tensor)

if torch.round(ans[0]) == 1.00:
    print("Correct!, the secret is " + secret)
else:
    print("Incorrect secret")
