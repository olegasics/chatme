from collections import namedtuple

from flask import Flask, render_template, redirect, request, url_for
from datetime import datetime
from models.models import User, Message, Room

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
    redirect(url_for('/main'))


@app.route('/main', methods=['GET'])
def main():
    return render_template('main.html')


@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.all()
    return render_template('messages.html', messages=messages)


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


@app.route('/messages', methods=['POST'])
def messages():
    text = request.form['text']
    time = datetime.datetime.now()
    message = Message(text=text, time=time)
    db.session.add(message)
    db.session.commit()

    # messages.append(Message(text, time))

    return redirect(url_for('messages'))


@app.route('/rooms', methods=['POST'])
def create_room():
    name = request.form['name']
    room = Room
