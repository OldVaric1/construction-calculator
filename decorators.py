from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_superuser:
            flash('Требуется статус суперпользователя для доступа', 'error')
            return redirect(url_for('products.list'))
        return f(*args, **kwargs)
    return decorated_function
