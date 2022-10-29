from gevent.pywsgi import WSGIServer
from flask import Flask, request, render_template, redirect
import requests
import time
import random
import os

app = Flask(__name__)

PROD = os.environ.get('PROD')
FLAG = os.environ.get('FLAG') or b'STDIO99{WINNER}'
app.config.update(
    CAPTCHA_SITE_KEY = os.environ.get("CAPTCHA_SITE_KEY"),
    CAPTCHA_SECRET_KEY = os.environ.get("CAPTCHA_SECRET_KEY"),
    PROMO_LEN = 5
)
PROMO_LEN = app.config["PROMO_LEN"]

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        data = {
            'secret': app.config["CAPTCHA_SECRET_KEY"],
            'response': request.form.get('g-recaptcha-response'),
            'remoteip': request.access_route[0]
        }
        r = requests.post(
            "https://www.google.com/recaptcha/api/siteverify",
            data=data
        )
        result = r.json()
        if not result['success']:
            error = "Nah wrong captcha. No bruteforce"
            return render_template('index.html', error=error)

        # random.seed(0) is so boomer
        # You don't know the server time? That's too bad.
        random.seed(int(time.time()))
        winningNum = random.randint(0,999999)
        try:
            pickNums = request.form["pickNum"].split(",")
            if len(pickNums) > PROMO_LEN:
                error = f'What are you doing? Only {PROMO_LEN} is allowed.'
                return render_template('index.html', error=error)
            for pickNum in pickNums:
                if int(pickNum) == winningNum:
                    error = f'WE HAVE A WINNER!! HERE A FLAG: {FLAG}'
                    return render_template('index.html', error=error)
        except Exception as e:
            print(e)
            error = "hmmm?"
            return render_template('index.html', error=error)

        error = f'Winner Number is... {winningNum} Try again next time :P {int(time.time())}'
        return render_template('index.html', error=error)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    if PROD:
        http_server = WSGIServer(("0.0.0.0", 1337), app)
        http_server.serve_forever()
    else:
        app.run(port=5000, debug=True)