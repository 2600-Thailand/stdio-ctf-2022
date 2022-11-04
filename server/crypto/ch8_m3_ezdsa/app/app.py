from gevent.pywsgi import WSGIServer
from flask import Flask, request, render_template, redirect
from ecdsa import SigningKey, NIST256p
import os
import re
import hashlib
import random
from hashlib import md5

app = Flask(__name__)

PROD = os.environ.get('PROD')
SK = SigningKey.generate(curve=NIST256p, hashfunc=hashlib.sha1)
VK = SK.verifying_key
FLAG = os.environ.get('FLAG') or b'STDIO99{NOT_THAT_EASY}'

def sanitize_number(n):
    return re.sub(r"[^0-9]", "", n)

def pad(msg):
    return msg + b"\x00" * (16 - len(msg)%16)

def entropy(n):
    # Our server has very low entropy pool. Dont use it too much
    r = os.urandom(1)
    while len(r) < n:
        r += md5(r).digest()
    
    return r[:n]


@app.route('/')
def index():
    error = request.args.get('error')
    amount = f"{random.randint(1,5)}"
    sig = SK.sign(amount.encode(), entropy=entropy)
    
    return render_template('index.html', error=error, amount=amount, example_code=f"{amount}:{sig.hex()}", version="V3")

@app.route('/airdrop', methods=['POST'])
def airdrop():
    code = request.form.get('code')
    _ = request.form.get('address')
    words = code.split(":")
    
    if len(words) != 2:
        return redirect("/?error=Invalid+code")
    
    msg = words[0]
    sig = words[1]
    
    try:
        VK.verify(bytes.fromhex(sig), msg.encode())
    except:
        return redirect("/?error=Invalid+code")
        
    amount = int(sanitize_number(msg))
    if amount >= 1337:
        return FLAG
    else:
        return redirect(f"/?error=Bankde+blockchain+can+only+transfer+coins+worth+more+than+or+equal+1337+({amount}<1337).")

if __name__ == '__main__':
    if PROD:
        http_server = WSGIServer(("0.0.0.0", 1337), app)
        http_server.serve_forever()
    else:
        app.run(port=5000, debug=True)
