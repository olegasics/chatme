import configparser

from flask import Flask
# from flask_cache import Cache
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


config = configparser.ConfigParser()
cfg = config.read('settings_dev.ini')

USER_NAME = config.get('database', 'bd_user')
PASSWORD = config.get('database', 'password_db')
DB_NAME = config.get('database', 'db_name')
SECRET_KEY = config.get('flask', 'secret_key')
APP_KEY = config.get('delin', 'appkey')
SESSION_ID = config.get('delin', 'sessionID')


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{USER_NAME}:{PASSWORD}@localhost:5432/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = SECRET_KEY
db = SQLAlchemy(app)
# cache = Cache(app)
migrate = Migrate(app, db)
