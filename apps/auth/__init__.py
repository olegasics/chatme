from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from db_config import DbConnectSingleton

db = DbConnectSingleton.get_instance()
app = DbConnectSingleton.get_instance().app

migrate = Migrate(app, db)