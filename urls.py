from apps.chat.views import MessageAPIView, RoomAPIView, MainAPIView
from apps.auth.views import UserAPIView, AuthAPIView, RegAPIView
from apps.chat.views import app
from flask_login import login_user, login_required

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from db_config import DbConnectSingleton

db = DbConnectSingleton.get_instance()
app = DbConnectSingleton.get_instance().app

migrate = Migrate(app, db)


def register_api(view, endpoint, url, pk='id', pk_type='int'):
    view_func = view.as_view(endpoint)
    app.add_url_rule(url, defaults={pk: None},
                     view_func=view_func, methods=['GET'])
    app.add_url_rule(url, view_func=view_func, methods=['POST'])
    app.add_url_rule('%s<%s:%s>' % (url, pk_type, pk), view_func=view_func,
                     methods=['GET', 'PUT', 'DELETE'])


register_api(UserAPIView, 'user_api', '/users/')

register_api(MessageAPIView, 'message_api', '/messages/', pk='message_text', pk_type='string')

register_api(RoomAPIView, 'room_api', '/rooms/', pk='room_id')


view_func_auth = AuthAPIView.as_view('auth_api')
app.add_url_rule('/login/', view_func=view_func_auth, methods=['GET', 'POST'])

view_func = RegAPIView.as_view('reg_api')
app.add_url_rule('/reg/', view_func=view_func, methods=['GET'])


