import sys
from extensions import db
from models.user import User

def create_superuser(username, password):
    with app.app_context():
        # Проверяем, не существует ли уже суперпользователь
        existing_superuser = User.query.filter_by(is_superuser=True).first()
        if existing_superuser:
            print(f"Суперпользователь уже существует: {existing_superuser.username}")
            return

        # Создаём нового пользователя с корректным хешированием
        user = User(username=username)
        user.set_password(password)
        user.is_superuser = True

        db.session.add(user)
        db.session.commit()
        print(f"Суперпользователь {username} успешно создан!")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Использование: python create_superuser.py <username> <password>")
    else:
        create_superuser(sys.argv[1], sys.argv[2])
