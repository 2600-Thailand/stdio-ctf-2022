from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort

from flaskr.auth import login_required, check_recaptcha
from flaskr.db import get_db
import uuid
import requests

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

@bp.route("/post")
@login_required
def post():
    """Check your own post."""
    db = get_db()
    id = g.user["id"]
    posts = db.execute(
        "SELECT p.id, uuid, title, body, created, author_id, username, mark_read"
        " FROM post p JOIN user u ON p.author_id = u.id"
        " WHERE (u.id = %s"  % (g.user["id"]) + ")"
        " ORDER BY created DESC"
    ).fetchall()
    return render_template("blog/post.html", posts=posts)

@bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    """Create a new post for the current user."""
    if request.method == "POST":
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
                "INSERT INTO post (uuid, title, body, author_id) VALUES (?, ?, ?, ?)",
                (str(uuid.uuid4()), title, body, g.user["id"]),
            )
            db.commit()
            return redirect(url_for("blog.index"))
    return render_template("blog/create.html")

@bp.route("/report", methods=["POST"])
@login_required
@check_recaptcha
def report():
    """Alert admin."""
    if request.recaptcha_is_valid != True:
        flash("Invalid reCAPTCHA. Please try again.")
        return redirect(url_for("blog.post"))

    id = request.form["uuid"]
    # validate for uuid
    try:
        id = str(uuid.UUID(id))
    except Exception as e:
        flash("What?")
        return redirect(url_for("blog.post"))

    # Alert post to admin, simulate admin to view
    requests.get(f'http://127.0.0.1:4000/?uuid={id}')

    return redirect(url_for("blog.post"))

@bp.route("/view", methods=["GET"])
@login_required
def view():
    """
    Show your the post of specify UUID.
    Temporary disable this feature from regular user.
    """
    if g.user["is_admin"] != 1:
        flash("Currently disable from normal user for security reason")
        return render_template("blog/index.html")
        
    db = get_db()
    posts = []
    if "uuid" in request.args:
        uuid = request.args["uuid"]
        posts = db.execute(
            "SELECT p.id, title, body, author_id, username"
            " FROM post p JOIN user u ON p.author_id = u.id"
            " WHERE uuid = '%s'" % (uuid)
        ).fetchall()
    return render_template("blog/view.html", posts=posts)