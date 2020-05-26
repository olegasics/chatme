from flask import render_template, redirect, request, url_for
from datetime import datetime
from apps.chat.models import Message, Room

import db_config
import datetime


db = db_config.DbConnectSingleton().get_instance()
app = db.app
db.create_all()


@app.route('/', methods=['GET'])
def start_page():

    """
    TODO to issue start page

    :return:
    """
    return redirect(url_for('main'))

@app.route('/main', methods=['GET'])
def main():
    return render_template('main.html')


@app.route('/reg', methods=['GET'])
def reg():
    return render_template('reg.html')


@app.route('/auth', methods=['GET'])
def auth():
    return render_template('auth.html')


@app.route('/info', methods=['GET'])
def info():
    return 'info'


@app.route('/tasks', methods=['GET'])
def tasks():
    return render_template('tasks.html')


# @app.route('/messages', methods=['POST'])
# def messages():
#     text = request.form['text']
#     time = datetime.datetime.now()
#     room_name = request.form['room']
#     room = Room.query.filter_by(name=room_name).first()
#     message = Message(text=text, time=time, room_id=room.id, user_id=1)
#     db.session.add(message)
#     db.session.commit()
#
#     return redirect(url_for('get_messages'))
#
#
# @app.route('/messages', methods=['GET'])
# def get_messages():
#     messages = Message.query.all()
#     rooms = Room.query.all()
#     return render_template('messages.html', messages=messages, rooms=rooms)


# @app.route('/rooms', methods=['POST'])
# def create_room():
#     name = request.form['name']
#     password = request.form['password']
#     room = Room(name=name, password=password)
#     db.session.add(room)
#     db.session.commit()
#     room = Room.query.filter_by(name=name).first()
#     return redirect(url_for('rooms', room_id=room.id))
#
#
# @app.route('/rooms/<int:room_id>', methods=['GET'])
# def rooms(room_id:int):
#     room = Room.query.filter_by(id=room_id).first()
#
#     if room.id:
#         return render_template('room.html', rooms=room)
#     else:
#         return '404'
