from functools import wraps

from flask import session, redirect, url_for, flash


def login_required():
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if not session.get('username'):
                flash('You must be logged in..', 'error')
                return redirect(url_for('login'))
            return f(*args, **kwargs)

        return wrapped

    return wrapper
