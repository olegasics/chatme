from flask import url_for, redirect
from flask_login import UserMixin, LoginManager

from db_config import db

login_manager = LoginManager(db.app)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    nick_name = db.Column(db.String(20), unique=True, nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('auth_api'))