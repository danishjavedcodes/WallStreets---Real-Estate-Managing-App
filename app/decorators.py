from functools import wraps

from flask import abort
from flask_login import current_user


def admin_required(*roles):
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(401)
            user_id = getattr(current_user, "get_id", lambda: None)()
            if not user_id or not str(user_id).startswith("admin:"):
                abort(403)
            if roles and current_user.user_type not in roles:
                abort(403)
            return view(*args, **kwargs)

        return wrapped

    return decorator


def customer_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(401)
        user_id = getattr(current_user, "get_id", lambda: None)()
        if not user_id or not str(user_id).startswith("customer:"):
            abort(403)
        return view(*args, **kwargs)

    return wrapped
