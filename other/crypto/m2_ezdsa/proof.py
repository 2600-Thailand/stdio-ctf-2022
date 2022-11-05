import requests
import re

possible = []

while True:
    r = requests.get("http://127.0.0.1:5000/")
    amount, r = re.findall(r" code \"([0-9]):(.+?)\"", r.text)[0]
    if r[:10] in possible:
        print("Good")
        exit()
    else:
        possible.append(r[:10])
        print(len(possible))