from gevent.pywsgi import WSGIServer
from flask import Flask, request, render_template, redirect
import hashlib2 as hashlib
import os
import re
import random

app = Flask(__name__)

PROD = os.environ.get('PROD')
KEY = os.urandom(16)
FLAG = os.environ.get('FLAG') or b'STDIO99{NOT_THAT_EASY}'
hashlib.make_it_harder()


def sanitize_number(n):
    return re.sub(r"[^0-9]", "", n)

@app.route('/debug')
def debug():
    msg = request.args.get('msg')
    return hashlib.notsha1(msg.encode()).hexdigest()
 
@app.route('/')
def index():
    error = request.args.get('error')
    amount = f"{random.randint(1,5)}"
    mac = hashlib.notsha1(KEY + amount.encode()).hexdigest()
    return render_template('index.html', error=error, amount=amount, example_code=f"{amount}:{mac}", version="V2")

@app.route('/airdrop', methods=['POST']) 
def airdrop():
    code = request.form.get('code')
    _ = request.form.get('address')
    words = code.split(":")
    
    if len(words) != 2:
        return redirect("/?error=Invalid+code")
    
    msg = words[0]
    mac = words[1]
    
    if mac != hashlib.notsha1(KEY + msg.encode('ascii', 'ignore')).hexdigest():
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
        app.run(port=5001, debug=True)