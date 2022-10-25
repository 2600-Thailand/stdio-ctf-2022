from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort

from flaskr.auth import login_required, admin_login_required
from flaskr.db import get_db

bp = Blueprint("admin", __name__, url_prefix='/admin')

@bp.route("/")
@login_required
@admin_login_required
def index():
    """Show the oldest post from user."""
    db = get_db()
    cursor = db.cursor()
    post = cursor.execute(
        "SELECT p.id, body, created, author_id, username"
        " FROM post p JOIN user u ON p.author_id = u.id"
        " WHERE u.is_admin != 1 AND p.mark_read = 0"
        " ORDER BY created ASC"
    ).fetchone()
    if post:
        pid = post["id"]
        # Mark as read show they won't show up again.
        cursor.execute(
            "UPDATE post SET mark_read = 1 WHERE id = " + str(pid)
        )
        db.commit()
    return render_template("admin/index.html", recent_post=post)