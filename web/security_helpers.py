# helper functions for secuity
from functools import wraps
import app
from flask import render_template, session


def sanitize_for_filename(filename):
    keepcharacters = [' ', '.', '_']
    safe = "".join(c for c in filename if c.isalnum()
                   or c in keepcharacters).rstrip()
    return safe.replace(" ", "_")


def check_auth(username):
    """This function is called to check if a username /
    password combination is valid.
    """
    print(username)
    record = app.app.config['db_cursor'].execute(
        "select * from users where username=?", (username,)).fetchone()
    if not record:
        return False
    return username == record[0]


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return render_template("autherr.html")


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not check_auth(session.get('username', None)):
            return authenticate()
        return f(*args, **kwargs)
    return decorated
