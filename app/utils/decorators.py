from functools import wraps
from flask import abort
from flask_login import current_user


def superuser_required(f):
    """
    Декоратор для ограничения доступа к маршруту только для суперпользователей.
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_superuser:
            abort(403)
        return f(*args, **kwargs)

    return decorated_function

