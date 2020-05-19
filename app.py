from collections import namedtuple

from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy

import datetime

app = Flask(__name__)
app.config['SQL_ALCHEMY_DATABASE'] = 'sqlite:////tmp/chat.db'
db = SQLAlchemy(app)

Message = namedtuple('Message', 'text time')
messages = []

@app.route('/', methods=['GET'])
def start_page():
    redirect(url_for('main'))


@app.route('/main', methods=['GET'])
def main():
    return render_template('main.html')


@app.route('/get_messages', methods=['GET'])
def get_messages():
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


@app.route('/add_message', methods=['POST'])
def add_message():
    text = request.form['text']
    time = datetime.datetime.now().strftime('%H:%M')

    messages.append(Message(text, time))

    return redirect(url_for('get_messages'))
