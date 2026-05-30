from extensions import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    unit_type = db.Column(db.String(20), default='м²')  # 'м²' или 'п.м.'
    category = db.Column(db.String(50), default='Прочие')
    coverage_per_unit = db.Column(db.Float, nullable=False) # Расход на единицу
    package_weight = db.Column(db.Float, default=30) # Вес упаковки
    image = db.Column(db.String(100), nullable=True, default='default.jpg')

    def __repr__(self):
        return f'<Product {self.name}>'
