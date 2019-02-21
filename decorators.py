from functools import wraps
from flask import session, url_for, redirect

def authenticate(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        auth = session.get("email")
        if not auth:
            return redirect(url_for("login")) #resp
        return func(*args, **kwargs)
    return decorated
