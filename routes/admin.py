from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user

admin_bp = Blueprint('admin', __name__, template_folder='../templates/admin')


@admin_bp.route('/dashboard')
@login_required
def dashboard():
    if not current_user.is_superuser:
        flash('Доступ запрещён: требуются права суперпользователя', 'error')
        return redirect(url_for('products.list'))
    return render_template('admin/dashboard.html')
