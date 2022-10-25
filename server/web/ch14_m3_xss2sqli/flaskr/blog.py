from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort

from flaskr.auth import login_required, admin_login_required, check_recaptcha
from flaskr.db import get_db

bp = Blueprint("blog", __name__)

@bp.route("/")
@login_required
def index():
    """Show admin annoucement."""
    db = get_db()
    id = g.user["id"]
    posts = db.execute(
        "SELECT p.id, title, body, created, author_id, username"
        " FROM post p JOIN user u ON p.author_id = u.id"
        " WHERE (u.is_admin == 1)"
        " ORDER BY created DESC"
    ).fetchall()
    return render_template("blog/index.html", posts=posts)

@bp.route("/history")
@login_required
def history():
    """Show your own post."""
    db = get_db()
    id = g.user["id"]
    posts = db.execute(
        "SELECT p.id, title, body, created, author_id, username, mark_read"
        " FROM post p JOIN user u ON p.author_id = u.id"
        " WHERE (u.id = %s"  % (g.user["id"]) + ")"
        " ORDER BY created DESC"
    ).fetchall()
    return render_template("blog/history.html", posts=posts)

@bp.route("/create", methods=["GET", "POST"])
@login_required
@check_recaptcha
def create():
    """Create a new post for the current user."""
    if request.method == "POST":
        if request.recaptcha_is_valid != True:
            flash("Invalid reCAPTCHA. Please try again.")
            return render_template("blog/create.html")
            
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "INSERT INTO post (title, body, author_id) VALUES (?, ?, ?)",
                (title, body, g.user["id"]),
            )
            db.commit()
            return redirect(url_for("blog.index"))
    return render_template("blog/create.html")

@bp.route("/search", methods=["GET"])
@login_required
@admin_login_required
def search():
    """
    Search for keyword.
    Temporary disable this feature from regular user.
    """
    db = get_db()
    id = g.user["id"]
    posts = []
    if "text" in request.args:
        text = request.args["text"]
        posts = db.execute(
            "SELECT p.id, title, body, author_id, username"
            " FROM post p JOIN user u ON p.author_id = u.id"
            " WHERE p.body LIKE '%" + text + "%'"
            " ORDER BY p.id ASC"
        ).fetchall()
    return render_template("blog/search.html", posts=posts)