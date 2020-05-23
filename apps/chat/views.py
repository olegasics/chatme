import db_config

from flask.views import MethodView
from flask import request
from datetime import datetime
from apps.chat.models import User, Room, Message


db = db_config.DbConnectSingleton.get_instance()
app = db.app


class UserAPI(MethodView):

    def get(self, user_id):
        if user_id is None:
            users = User.query.all()
        else:
            return str(User.query.filter_by(id=user_id).first().id)

    def post(self):
        text = request.form['text']
        time = datetime.datetime.now()
        room_name = request.form['room']
        room = Room.query.filter_by(name=room_name).first()
        message = Message(text=text, time=time, room_id=room.id, user_id=1)
        db.session.add(message)
        db.session.commit()

    def put(self, user_id):
        pass

    def delete(self, user_id):
        pass


class MessageAPI(MethodView):
    def get(self, message_id):
        if message_id is None:
            pass
        else:
            pass

    def post(self):
        pass

    def put(self, message_id):
        pass

    def delete(self, message_id):
        pass


class RoomAPI(MethodView):
    def get(self, room_id):
        if room_id is None:
            pass
        else:
            pass

    def post(self):
        pass

    def put(self, room_id):
        pass

    def delete(self, room_id):
        pass