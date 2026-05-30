from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class ProductForm(FlaskForm):
    name = StringField('Название товара', validators=[DataRequired()])
    price = FloatField('Цена', validators=[DataRequired()])

    category = SelectField(
        'Категория',
        choices=[
            ('Забор', 'Забор'),
            ('Кровля', 'Кровля'),
            ('Штукатурка', 'Штукатурка'),
            ('Шпаклёвка', 'Шпаклёвка'),
            ('Прочие', 'Прочие')
        ],
        default='Прочие'
    )

    coverage_per_unit = FloatField(
        'Расход на единицу',
        validators=[
            DataRequired(),
            NumberRange(min=0.01, message='Покрытие должно быть положительным числом')
        ]
    )
    unit_type = SelectField(
        'Единица измерения',
        choices=[('м²', 'м² (квадратный метр)'), ('п.м.', 'п.м. (погонный метр)')],
        validators=[DataRequired()]
    )
    package_weight = StringField('Вес упаковки (кг)', default=30)
    image = FileField('Фото товара', validators=[
                FileAllowed(['jpg', 'png', 'jpeg'], 'Только изображения!')
    ])
    submit = SubmitField('Добавить')