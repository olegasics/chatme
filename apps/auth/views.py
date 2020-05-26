import db_config

from flask.views import MethodView
from flask import render_template, redirect, request, url_for, flash, session, abort
from flask_login import login_user
from werkzeug.security import check_password_hash, generate_password_hash

from apps.auth.models import User

db = db_config.DbConnectSingleton.get_instance()
app = db.app


class UserAPIView(MethodView):

    def get(self, id):
        login = request.form['login']
        password = request.form['password']

        if login and password:
            user = User.query.filter_by(login=login).first()

            if check_password_hash(user.password, password):
                login_user(user)

                return redirect(url_for('message_api'))
            else:
                flash('Login or password is not correct. Try again')
        else:
            flash('Please enter login and password fields')

    def post(self):

        login = request.form['login']
        password = request.form['password']
        password2 = request.form['password2']
        nick_name = request.form['nickname']

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


class AuthAPIView(MethodView):
    def get(self):
        return render_template('login.html')

    def post(self):
        login = request.form['login']
        password = request.form['password']

        if login and password:
            user = User.query.filter_by(login=login).first()

            if check_password_hash(user.password, password):
                login_user(user)
                # if user.password == password:
                #     login_user(user)
                session['userLogged'] = login
                return redirect(url_for('message_api'))
            else:
                flash('Login or password is not correct. Try again')
                return render_template('login.html')
        else:
            flash('Please enter login and password fields')
            return render_template('login.html')
        # login = request.form.get('login')
        # password = request.form.get('password')
        # with app.test_request_context():
        #     print(url_for('user_api', login=login, password=password))
        # return redirect(url_for('user_api', login=login, password=password))

class RegAPIView(MethodView):
    def get(self):
        return render_template('reg.html')
