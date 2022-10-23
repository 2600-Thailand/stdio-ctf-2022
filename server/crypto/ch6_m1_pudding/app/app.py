from gevent.pywsgi import WSGIServer
from flask import Flask, request, render_template, redirect
from Crypto.Cipher import AES
import os
import re
import random

app = Flask(__name__)

PROD = os.environ.get('PROD')
KEY = os.urandom(16)
FLAG = os.environ.get('FLAG') or b'STDIO99{NOT_THAT_EASY}'
 
def sanitize_number(n):
    return re.sub(r"[^0-9]", "", n)

def pad(msg):
    return msg + b"\x00" * (16 - len(msg)%16)

@app.route('/')
def index():
    error = request.args.get('error')
    iv = os.urandom(16)
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    amount = f"{random.randint(1,5)}"
    code = cipher.encrypt(pad(amount.encode()))
    
    return render_template('index.html', error=error, amount=amount, example_code=f"{iv.hex()}{code.hex()}", version="V1")

@app.route('/airdrop', methods=['POST'])
def airdrop():
    code = request.form.get('code')
    _ = request.form.get('address')
    
    iv = bytes.fromhex(code[:32])
    ct = bytes.fromhex(code[32:])
    
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    pt = sanitize_number(cipher.decrypt(ct).decode('ascii', 'ignore'))
    
    if len(pt) == 0:
        return redirect("/?error=Invalid+code")
    
    amount = int(pt)
    if amount >= 1337:
        return FLAG
    else:
        return redirect(f"/?error=Bankde+blockchain+can+only+transfer+coins+worth+more+than+or+equal+1337+({amount}<1337).")

if __name__ == '__main__':
    if PROD:
        http_server = WSGIServer(("0.0.0.0", 1337), app)
        http_server.serve_forever()
    else:
        app.run(port=5001, debug=True)
        