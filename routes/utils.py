from functools import wraps
from flask import g, redirect, url_for

def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('user.login'))
        return view(**kwargs)
    return wrapped_view

def admin_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None or g.user['role'] != 'admin':
            return redirect(url_for('home'))
        return view(**kwargs)
    return wrapped_view
