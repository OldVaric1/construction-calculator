from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required
from forms import LoginForm, RegisterForm
from models import User, user
from extensions import db

auth_bp = Blueprint('auth', __name__, template_folder='../templates/auth')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Вы успешно вошли!', 'success')
            return redirect(url_for('products.list'))
        else:
            flash('Неверное имя пользователя или пароль', 'error')
    return render_template('auth/login.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Пользователь с таким именем уже существует', 'error')
            return render_template('register.html', form=form)

        try:
            user = User(username=form.username.data)
            user.set_password(form.password.data)

            db.session.add(user)
            db.session.commit()
            flash(f'Ваш аккаунт {form.login.data} был создан!', 'success')
            return redirect(url_for('aurh.login'))
        except Exception as e:
            flash(f'При регистрации произошла ошибка!', 'danger')
    return render_template('auth/register.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('products.list'))
