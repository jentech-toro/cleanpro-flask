from functools import wraps
from flask import session, redirect, url_for


def require_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("admin"):
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated
