import os


UPLOAD_FOLDER = os.path.join('static', 'images')

class Config(object):
    APPNAME = 'app'
    ROOT = os.path.abspath(APPNAME)
    UPLOAD_PATH = '/static/upload/'
    SERVER_PATH = ROOT + UPLOAD_PATH

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

    if SQLALCHEMY_DATABASE_URI:
        # Для совместимости с Render: заменяем postgres:// на postgresql://
        if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
            SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)
    else:
        # Локальная база (если DATABASE_URL не задан)
        USER = os.environ.get('POSTGRES_USER', 'postgres')
        PASSWORD = os.environ.get('POSTGRES_PASSWORD', '03sz2003988')
        HOST = os.environ.get('POSTGRES_HOST', '127.0.0.1')
        PORT = os.environ.get('POSTGRES_PORT', '5532')
        DB = os.environ.get('POSTGRES_DB', 'postgres')
        SQLALCHEMY_DATABASE_URI = f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}'
    SECRET_KEY = 'asd3rgfg4323fsgsdfgfh6u445yrehdfh'
    SQLALCHEMY_TRACK_MODIFICATIONS = True