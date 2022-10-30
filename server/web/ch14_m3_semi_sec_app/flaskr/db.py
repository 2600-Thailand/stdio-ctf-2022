import sqlite3
import click
from flask import current_app
from flask import g
from werkzeug.security import generate_password_hash
import datetime

import uuid

def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    """If this request connected to the database, close the
    connection.
    """
    db = g.pop("db", None)

    if db is not None:
        db.close()

def init_db():
    """Clear existing data and create new tables."""
    db = get_db()

    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))

def init_ctf_db():
    db = get_db()
    cursor = db.cursor()
    """Add default admin account"""
    cursor.execute(
        "INSERT INTO user (username, password, is_admin) VALUES (?, ?, 1)",
        ("admin", generate_password_hash(current_app.config.get("ADMIN_PASSWORD"))),
    )
    """Add CTF Flag"""
    cursor.execute(
        "INSERT INTO user (username, password, is_admin) VALUES (?, ?, 1)",
        ("owner", current_app.config.get("CTF_FLAG")),
    )
    owner_id = cursor.lastrowid # Should be 2
    """Add starting data"""
    cursor.execute(
        "INSERT INTO post (title, body, author_id, created, uuid) VALUES (?, ?, ?, ?, ?)",
        ("BLOG ANNOUCEMENT", 
        "WELCOME TO LONGCAT FANCLUB BLOG.\nYou can create your own post and even brag them to admin group.", 
        owner_id,
        datetime.datetime(2022,10,1,0,0,0,0),
        str(uuid.uuid4()),)
    )
    cursor.execute(
        "INSERT INTO post (title, body, author_id, created, uuid) VALUES (?, ?, ?, ?, ?)",
        ("VIEW FUNCTION REMOVED", 
        "Thank to Ad'Earth's security report, we temporary limit the view function to admin only.", 
        owner_id,
        datetime.datetime(2022,10,3,0,0,0,0),
        str(uuid.uuid4()),)
    )
    cursor.execute(
        "INSERT INTO post (title, body, author_id, created, uuid) VALUES (?, ?, ?, ?, ?)",
        ("FEATURE UPDATE", 
        "<center>Allowing HTML tags are cool. LOOK!!</center><br><marquee>WHEEEEEEEEEEEEEEEEEEEEEEEEEEE<br><img src='/static/images/longcat.jpg' height='300px'></marquee><br><center><br>Don't worry, our cookie is HTTPonly so we are safe from document.cookie XSS.</center>", 
        owner_id,
        datetime.datetime(2022,10,8,0,0,0,0),
        str(uuid.uuid4()),)
    )
    cursor.execute(
        "INSERT INTO post (title, body, author_id, created, uuid) VALUES (?, ?, ?, ?, ?)",
        ("LONGCAT ARMSTRONG CYCLONE JET ARMSTRONG CANNON", 
        "<center><img src='/static/images/Longcat_War.jpg'></center>", 
        owner_id,
        datetime.datetime(2022,10,9,0,0,0,0),
        str(uuid.uuid4()),)
    )
    db.commit()

@click.command("init-db")
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    init_ctf_db()
    click.echo("Initialized the database.")

def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
