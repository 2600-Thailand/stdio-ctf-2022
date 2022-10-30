import functools
from re import T

from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from flaskr.db import get_db

import requests
from flask import current_app

from base64 import b64encode
from os import urandom

bp = Blueprint("auth", __name__, url_prefix="/auth")

def login_required(view):
    """View decorator that redirects anonymous users to the login page."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            error = "You need to login first."
            flash(error)
            return redirect(url_for("auth.login"))
        return view(**kwargs)
    return wrapped_view

def check_recaptcha(view):
    """
    Cheks Google reCAPTCHA
    """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        request.recaptcha_is_valid = None
        if request.method == "POST":
            data = {
                'secret': current_app.config.get("CAPTCHA_SECRET_KEY"),
                'response': request.form.get('g-recaptcha-response'),
                'remoteip': request.access_route[0]
            }
            r = requests.post(
                "https://www.google.com/recaptcha/api/siteverify",
                data=data
            )
            result = r.json()
            if result['success']:
                request.recaptcha_is_valid = True
            else:
                request.recaptcha_is_valid = False
        return view(**kwargs)
    return wrapped_view

@bp.before_app_request
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        g.user = (
            get_db().execute("SELECT * FROM user WHERE id = ?", (user_id, )).fetchone()
        )

@bp.route("/register", methods=["GET", "POST"])
def register():
    """Register a new user.

    Validates that the username is not already taken. Hashes the
    password for security.
    """
    if request.method == "POST":
        username = request.form["username"]
        password = b64encode(urandom(32)).decode('utf-8')

        db = get_db()
        error = None

        if not username:
            error = "Username is required."
            flash(error)
            return render_template("auth/register.html")

        try:
            db.execute(
                "INSERT INTO user (username, password) VALUES (?, ?)",
                (username, generate_password_hash(password)),
            )
            db.commit()
        except db.IntegrityError:
            # The username was already taken, which caused the
            # commit to fail. Show a validation error.
            error = f"User {username} is already registered."
            return render_template("auth/register.html")
        else:
            # Success, go to the login page.
            flash("Your password is %s" % (password))
            return redirect(url_for("auth.login"))

    return render_template("auth/register.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    """Log in a registered user by adding the user id to the session."""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None
        user = db.execute(
            "SELECT * FROM user WHERE username = ?", (username,)
        ).fetchone()

        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user["password"], password):
            error = "Incorrect password."

        if error is None:
            # store the user id in a new session and return to the index
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("index"))

        flash(error)

    return render_template("auth/login.html")

@bp.route("/logout")
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for("auth.login"))
