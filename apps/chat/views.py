import db_config

from flask.views import MethodView
from flask import render_template, redirect, request, url_for, flash, session, abort
from flask_login import login_user
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash

from apps.chat.models import Room, Message
from apps.auth.models import User

db = db_config.DbConnectSingleton.get_instance()
app = db.app


class UserAPIView(MethodView):

    def get(self, user_id):

        login = request.form.get('login')
        password = request.form.get('password')

        if login and password:
            user = User.query.filter_by(login=login).first()

            if check_password_hash(user.password, password):
                login_user(user)

                # save previous url for user and redirect him after auth
                next_page = request.args.get('next')

                return redirect(next_page)
            else:
                flash('Login or password is not correct. Try again')
        else:
            flash('Please enter login and password fields')


    def post(self):
        login = request.form['login']
        password = request.form['password']
        password2 = request.form['password2']
        nick_name = request.form('nickname')

        if not (login or password or password2):
            flash('Please, enter all fields!')
        elif password2 != password:
            flash('Passwords are not equals!')
        else:
            hash_pwd = generate_password_hash(password)
            new_user = User(login=login, password=hash_pwd, nick_name=nick_name)
            db.session.add(new_user)
            db.session.commit()
        return render_template('login.html')

    def put(self, user_id):
        pass

    def delete(self, user_id):

        pass


class MessageAPIView(MethodView):
    def get(self, message_text):
        if message_text is None:
            # login = request.form['login']
            # if 'userLogged' not in session or session['userLogged'] != login:
            #     abort(401)
            rooms = Room.query.all()
            messages = Message.query.all()
            return render_template('messages.html', messages=messages, rooms=rooms)
        return '1'

    def post(self):
        text = request.form['text']
        room_id = request.form['room_id']

        room = Room.query.get(room_id)
        message = Message(text=text, room_id=room.id, user_id=1)
        db.session.add(message)
        db.session.commit()

        return redirect(url_for('room_api') + room_id)
        # return render_template('room.html', messages=messages, room=room)

    def put(self, message_id):
        pass

    def delete(self, message_id):
        pass


class RoomAPIView(MethodView):
    def get(self, room_id):
        if room_id is None:
            pass
        else:
            messages = Message.query.filter_by(room_id=room_id)
            room = Room.query.get(room_id)
            return render_template('room.html', room=room, messages=messages)

    def post(self):
        name = request.form['name']
        password = request.form['password']
        room = Room(name=name, password=password)
        db.session.add(room)
        db.session.commit()
        room = Room.query.filter_by(name=name).first()
        return render_template('room.html', room=room)

    def put(self, room_id):
        pass

    def delete(self, room_id):
        pass


class MainAPIView(MethodView):

    def get(self):
        return render_template('main.html')

    def post(self):
        pass

    def put(self, message_id):
        pass

    def delete(self, message_id):
        pass
