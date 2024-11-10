from functools import wraps
from flask import session,redirect, url_for

def auth_user(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('/'))
        return f(*args, **kwargs)
    return decorated_function