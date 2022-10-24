
secret = b"Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."
key = b'STDIO05{72d8c669d5be54c29e797668ea4b505e}'


def rxor(msg, key):
    r = []
    for i,m in enumerate(msg):
        r.append(m ^ key[i % len(key)])
    
    return bytes(r)

ct = rxor(secret, key)
assert rxor(ct, key) == secret

f = open("../../../file/ch5_mtp.txt", "w")
f.write(ct.hex())
f.close()

