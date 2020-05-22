from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import configparser

config = configparser.ConfigParser()
cfg = config.read('settings_dev.ini')

USER_NAME = config.get('database', 'bd_user')
PASSWORD = config.get('database', 'password_db')
DB_NAME = config.get('database', 'db_name')


class DbConnectSingleton:
    """
    return instance db connection
    """
    __instance = None

    @staticmethod
    def get_instance():
        if DbConnectSingleton.__instance == None:
            app = Flask(__name__)
            app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://chat_admin:edcvfr12!@localhost:5432/chat_db'
            app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
            return SQLAlchemy(app)
        return DbConnectSingleton.__instance

    def __init__(self):
        if DbConnectSingleton != None:
            DbConnectSingleton.__instance = self.get_instance()
        else:
            DbConnectSingleton.__instance = self