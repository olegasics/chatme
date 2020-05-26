from datetime import datetime
from flask_login import UserMixin, LoginManager

import db_config

db = db_config.DbConnectSingleton().get_instance()
login_manager = LoginManager(db.app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    nick_name = db.Column(db.String(20), unique=True, nullable=False)
