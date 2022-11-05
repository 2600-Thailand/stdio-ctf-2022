import os

secret = os.getenv("SECRET").encode()
key = os.getenv("KEY").encode()

def rxor(msg, key):
    r = []
    for i,m in enumerate(msg):
        r.append(m ^ key[i % len(key)])
    
    return bytes(r)

ct = rxor(secret, key)
assert rxor(ct, key) == secret

f = open("ch5_mtp.txt", "w")
f.write(ct.hex())
f.close()

