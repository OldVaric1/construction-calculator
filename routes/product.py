import logging
import os

from flask import Blueprint, render_template, request, flash, redirect, url_for, abort, current_app
from flask_login import login_required, current_user
from functools import wraps

from werkzeug.utils import secure_filename

from decorators import admin_required
from forms import ProductForm
from extensions import db
from models import User, Product
from utils.calculator import SafeCalculator
from utils.utils import save_uploaded_file

products_bp = Blueprint('products', __name__, template_folder='../templates/products')

def superuser_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Для доступа требуется авторизация', 'error')
            return redirect(url_for('auth.login'))
        if not current_user.is_superuser:
            flash('У вас нет прав для выполнения этого действия', 'error')
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@products_bp.route('/')
def list():
    products = Product.query.all()
    # Группируем товары по категориям
    categories = {}
    for product in products:
        if product.category not in categories:
            categories[product.category] = []
        categories[product.category].append(product)
    return render_template('list.html', categories=categories)

@products_bp.route('/detail/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id) # Получаем товар или ошибку 404
    if not product.image:
        product.image = 'default.jpg'
    return render_template('products/detail.html', product=product)

@products_bp.route('/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add():
    form = ProductForm()
    if request.method == 'POST':
        filename = None
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            # Формируем полный путь к папке static/images
            upload_folder = os.path.join(current_app.static_folder, 'images')
            os.makedirs(upload_folder, exist_ok=True)
            # Сохраняем файл
            form.image.data.save(os.path.join(upload_folder, filename))

        # Получаем данные из формы
        name = request.form.get('name')
        category = request.form.get('category')
        price = request.form.get('price')
        unit_type = request.form.get('unit_type')
        coverage = request.form.get('coverage_per_unit')
        package_weight = request.form.get('package_weight')
        image =filename

        product = Product(name=name, category=category, price=price, unit_type=unit_type, coverage_per_unit=coverage, package_weight=package_weight, image=image)
        db.session.add(product)
        db.session.commit()
        flash('Товар добавлен!', 'success')
        if not current_user.is_superuser:
            flash('Доступ запрещён: требуются права суперпользователя', 'error')
            return redirect(url_for('products.list'))
    return render_template('products/add.html', form=form)



@products_bp.route('/edit/<int:product_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit(product_id):
    product = Product.query.get_or_404(product_id)
    form = ProductForm(obj=product)

    if form.validate_on_submit():
        # Сначала заполняем все поля из формы
        form.populate_obj(product)

        # Затем обрабатываем изображение — если загружено новое, обновляем
        new_image = save_uploaded_file(form.image.data, current_app.config['UPLOAD_FOLDER'])
        if new_image is not None:
            product.image = new_image

        db.session.commit()
        flash('Товар успешно обновлён!', 'success')
        return redirect(url_for('products.list'))

    return render_template('products/edit.html', form=form, product=product)



@products_bp.route('/delete/<int:id>')
@login_required
@superuser_required
def delete(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash('Товар удалён!', 'success')
    return redirect(url_for('products.list'))




