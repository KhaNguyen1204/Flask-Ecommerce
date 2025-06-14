from functools import wraps
from flask import session, flash, redirect, url_for
from shop.models import User

def role_required(allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'email' not in session:
                flash('Hãy đăng nhập để truy cập trang.', 'danger')
                return redirect(url_for('login'))

            user = User.query.filter_by(email=session['email']).first()
            if not user or user.role.name not in allowed_roles:
                flash('Bạn không có quyền truy cập trang.', 'danger')
                return redirect(url_for('home'))

            return f(*args, **kwargs)
        return decorated_function
    return decorator