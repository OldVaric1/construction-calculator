import os

from flask import Flask
from sqlalchemy import select

from config import Config
from extensions import db
from flask_migrate import Migrate
from flask_login import LoginManager

from models import User
from routes.calculator import calculator_bp

migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'images')

    # Инициализация расширений
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        from models.user import User
        return db.session.get(User, int(user_id))

    # Регистрация blueprints
    from routes.auth import auth_bp
    from routes.product import products_bp
    from routes.admin import admin_bp

    app.register_blueprint(calculator_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(products_bp)

    return app






if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
        if not db.session.scalars(select(User)).first():
            superuser = User(
                username='admin',
                is_superuser=True
            )
            superuser.set_password('admin123')
            db.session.add(superuser)
            db.session.commit()
    app.run(debug=True)

# Создаём приложение для WSGI
app = create_app()

# Создаём таблицы и суперпользователя при запуске, если их нет
with app.app_context():
    from extensions import db
    from models import User
    from sqlalchemy import select
    
    # Создаём все таблицы, если они ещё не существуют
    db.create_all()
    
    # Создаём суперпользователя, если нет ни одного
    if not db.session.scalars(select(User)).first():
        superuser = User(username='admin', is_superuser=True)
        superuser.set_password('admin123')
        db.session.add(superuser)
        db.session.commit()
