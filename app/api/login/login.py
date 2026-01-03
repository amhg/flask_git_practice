from flask import current_app, jsonify, request, Response, abort, session, make_response, render_template, flash
from flask.json import dumps, loads
from flask.json.provider import JSONProvider
from app.model.db import Login
from app.repository.login import LoginRepository
from app.model.config import db_session
from app.model.models import LoginForm, LoginAuthForm
from app.repository.repo_provider import get_repo_provider

import datetime
import asyncio
import time
import threading
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@current_app.route("/loginrebase")
def profile():
    print("Login request received")
    return "login demo rebase"


@current_app.route('/testform', methods = ['GET', 'POST'])
def test_form():
    if request.method == 'GET':
        return """
                <form action="http://127.0.0.1:5005/testform" method="POST">
                <input type="text" name="username">
                <input type="password" name="password">
                <input type="submit">
                </form>
                """
    else:
        print(f'request form: {request.form}')
        return make_response({"msg": "is a post"})
    


@current_app.route('/login/add', methods = ['GET','POST'])
def add_login():
    form:LoginForm = LoginForm()
    
    #logger.debug(f"CSRF token in form: {form.csrf_token.data}")

    if form.validate_on_submit(): 
        username = form.username.data
        print(username)

        with get_repo_provider(LoginRepository) as repo:
            login = Login(username= form.username.data,
                          password = form.password.data,
                          user_type = int(form.user_type.data[0]))
            
            result = repo.insert(login)
            if result:
                #records = repo.select_all()
                return jsonify(message = "New User added")
                #return render_template('login_list.html', records=records), 200
            else:
                return jsonify(message = "A problem occur")
                #return render_template('login_add.html', records=records), 500     
    return render_template('login_add.html', form=form)


@current_app.route('/login/auth', methods = ['GET', 'POST'])
def login_db_auth():
    authForm: LoginAuthForm = LoginAuthForm()
    print(f'in POST Login/auth: {dict(session)}')
    print(f'Request form data: {str(request.form)}')

    if authForm.validate_on_submit():
        repo = LoginRepository(db_session)
        username = authForm.username.data
        password = authForm.password.data
        user:Login = repo.select_one_username(username)

        if user == None:
            return render_template('login.html', form=authForm), 500
        elif not user.password == password:
            return render_template('login.html', form=authForm), 500
        else:
           session['username'] = username
           print('cookie: ' + session['username'])
           #response.headers
           return render_template('test_template.html')
    return render_template('login.html', form=authForm)


@current_app.get('/logout')
def logout():
    print(f'cookie session: {dict(session)}')
    session.pop('username')
    print(f'After pop cookie session: {dict(session)}')
    return jsonify({'message': 'User is logged'}), 200


@current_app.route('/set_theme')
def set_theme_cookie():
    response = make_response('', 204)  # No need to return full HTML
    response.set_cookie('theme', 'dark', max_age=60*60*24*30)
    return response

@current_app.route('/test_template')
def show_template():
    theme = request.cookies.get('theme', 'light')
    return render_template('test_template.html', theme=theme)



@current_app.get('/unsafe/<string:username>')
def get_unsafe(username:str):
    print(f'CSRF: {session['csrf_token']} ')
    print(f'cookie session: {dict(session)}')

    repo = LoginRepository(db_session)
    result = repo.select_one_username_unsafe(username)
    return render_template('login_list.html', result=result)


@current_app.patch('/login/password/update/<string:username>')
def update_password(username:str):
    session['username'] = username
    login_json = request.get_json()
    repo = LoginRepository(db_session)
    result = repo.update(username, login_json)
    if result:
        current_app.logger.info('user details updated')
        return jsonify(login_json)

    else:
        abort(500, description="problem with updating user information")

@current_app.route('/login/list/all', methods = ['GET'])
def list_all_login():
    repo = LoginRepository(db_session)
    records = repo.select_all()
    login_rec = [rec.to_json() for rec in records]
    resp = Response(response = dumps(login_rec), status=200, mimetype="application/json")
    return resp



@current_app.post('/login')
def login():
    if request.is_json:
        login_json = request.get_json()
        username = login_json.get('username')
        password = login_json.get('password')
        
        #repo = LoginRepository(db_session)
        #user = repo.select_one_username(username)
        #current_app.logger.info('USER: %s', user)

        # Simulate user lookup 
        if username == 'admin' and password == '123':
            session['user_id'] = 1
            session['username'] = username
            print(f'in POST Login session: {dict(session)}')
            return jsonify({'message': 'Logged in successfully'}), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401

    return jsonify({'error': 'Invalid request'}), 400

@current_app.get('/dashboard')
def dashboard():
    print(f'in Dashboard: {dict(session)}')
    user_id = session.get('user_id')
    if user_id:
        return jsonify({'message': f'Welcome back, user {user_id}!'}), 200
    else:
        return jsonify({'error': 'Not logged in'}), 401
    

"""

@current_app.route('/session')
def get_session():
    return 'No session used'

@current_app.route('/set')
def set_session():
    session['key'] = 'value'
    return 'Session set'

@current_app.get('/setcookie')
def set_cookie():
    response = make_response('Cookie is set')
    response.set_cookie('username', 'flask_user')
    return response

@current_app.get('/getcookie')
def get_cookie():
    username = request.cookies.get('username')
    return f'Cookie value is: {username}'

"""


"""
#CSRF
@current_app.route("/api/get-csrf-token", methods=["GET"])
def get_csrf_token():
    response = make_response(jsonify({"message": "Token set"}))
    response.set_cookie("X-CSRFToken", generate_csrf(), httponly=False, secure=False)
    return response
"""


"""
    if request.is_json:
        login_json = loads(request.data)
        login = Login(**login_json)
        repo = LoginRepository(db_session)
        result = repo.insert(login)
        if result:
            current_app.logger.info('insert login credentials successful')
            return jsonify(login_json)
        else:
            abort(500, description="insert login encountered a problem")

    else:
        abort(500)
"""
