from flask import Blueprint, render_template, request, flash
from flask_login import login_required

from models import Product

calculator_bp = Blueprint('calculator', __name__, template_folder='../templates/calculator')



# Калькулятор расчёта сухих смесей
@calculator_bp.route('/calculator/mix', methods=['GET', 'POST'])
@login_required
def mix_calculator():
    # Фильтруем только сухие смеси
    mix_categories = ['Штукатурка', 'Шпаклёвка', 'Наливной пол', 'Клей для плитки']
    products = Product.query.filter(Product.category.in_(mix_categories)).all()

    selected_product_id = None
    if request.method == 'POST':
        selected_product_id = request.form.get('product_id')

    result = None
    error = None
    area = None
    thickness = None


    if request.method == 'POST':
        try:
            product_id = request.form.get('product_id')
            area_str = request.form.get('area', '1')
            thickness_str = request.form.get('thickness', '1')

            # Проверка выбора продукта
            if not product_id:
                error = 'Выберите сухую смесь из списка'
                return render_template('calculator/mix_calculator.html',
                   products=products, result=result, error=error,
                   area=area, thickness=thickness, selected_product_id=product_id)

            # Находим продукт по ID
            product = Product.query.get(product_id)
            if not product:
                error = 'Продукт не найден'
                return render_template('calculator/mix_calculator.html',
                   products=products, result=result, error=error,
                   area=area, thickness=thickness, selected_product_id=product_id)

            # Валидация площади
            try:
                area = float(area_str)
                if area <= 0:
                    error = 'Площадь должна быть положительным числом'
                    return render_template('calculator/mix_calculator.html',
                       products=products, result=result, error=error,
                       area=area, thickness=thickness, selected_product_id=product_id)
            except ValueError:
                error = 'Введите корректное значение площади'
                return render_template('calculator/mix_calculator.html',
                   products=products, result=result, error=error,
                   area=area, thickness=thickness, selected_product_id=product_id)

            # Валидация толщины
            try:
                thickness = float(thickness_str)
                if thickness <= 0:
                    error = 'Толщина должна быть положительным числом'
                    return render_template('calculator/mix_calculator.html',
               products=products, result=result, error=error,
               area=area, thickness=thickness, selected_product_id=product_id)
            except ValueError:
                error = 'Введите корректное значение толщины'
                return render_template('calculator/mix_calculator.html',
                   products=products, result=result, error=error,
                   area=area, thickness=thickness, selected_product_id=product_id)

            # Расчёт расхода сухой смеси
            total_consumption = area * thickness * product.coverage_per_unit # кг
            # Расчёт количества упаковок
            import math
            packages_needed = math.ceil(total_consumption / product.package_weight)
            total_price = packages_needed * product.price

            result = {
                'total_kg': round(total_consumption, 2),
                'packages': packages_needed,
                'product_name': product.name,
                'package_weight': product.package_weight,
                'total_price': round(total_price, 2)
            }

        except Exception as e:
            error = f'Ошибка вычислений: {str(e)}'
            return render_template('calculator/mix_calculator.html',
               products=products, result=result, error=error,
               area=area, thickness=thickness, selected_product_id=product_id)


    return render_template('calculator/mix_calculator.html',
               products=products,
               result=result,
               error=error,
               area=area,
               thickness=thickness,
               selected_product_id=selected_product_id)

# Заглушки для других калькуляторов
@calculator_bp.route('/calculator/siding', methods=['GET', 'POST'])
@login_required
def siding_calculator():
    return render_template('calculator/siding_calculator.html')

@calculator_bp.route('/calculator/fence', methods=['GET', 'POST'])
@login_required
def fence_calculator():
    return render_template('calculator/fence_calculator.html')

@calculator_bp.route('/calculator/roof', methods=['GET', 'POST'])
@login_required
def roof_calculator():
    return render_template('calculator/roof_calculator.html')
