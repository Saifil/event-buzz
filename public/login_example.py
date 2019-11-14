from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo

import database.data.mongo_setup as mongo_setup
import database.services.data_service as svc

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'eventbuzz'
app.config['MONGO_URI'] = 'mongodb://127.0.0.1:27017/eventbuzz'

mongo = PyMongo(app)


@app.route('/')
def index():
    # if 'email' in session:
    #     # redirect user to his event page
    #     return 'You are logged in as ' + session['email']

    return render_template('index.html')
    # return render_template('signup.html')
    # return render_template('login.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = svc.get_user_info(email, password)
        if user is not None:
            session['email'] = user.email
            # return 'You are logged in as ' + session['email']
            # return render_template('event_data.html')
            return redirect(url_for('events'))
        else:
            return render_template('login.html')
    return render_template('login.html')


@app.route('/events', methods=['POST', 'GET'])
def events():
    event_list = svc.get_all_event_data()

    return render_template('event_data.html', data=event_list[:6])


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        age = request.form['age']
        educ = request.form['educ']
        major = request.form['major']

        print(f"Name: {name}")

        users = svc.get_user_info(email, password)
        if users is None:
            new_usr = svc.create_new_user(name, email, password, age, educ, major)
            session['email'] = new_usr.email
            return redirect(url_for('index'))
            # return render_template('index.html')

        # if existing_user is None:
        #     # hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
        #     users.insert({'name': request.form['username'], 'password': hashpass})
        #     session['username'] = request.form['username']
        #     return redirect(url_for('index'))

        return 'That username already exists!'

    return render_template('signup.html')
    # return render_template('register.html')


# @app.route('/register', methods=['POST', 'GET'])
# def register():
#     if request.method == 'POST':
#
#         users = svc.get_user_info(request.form['username'], request.form['pass'])
#         if users is None:
#             new_usr = svc.create_new_user(request.form['username'], 'sm@mail.com', request.form['pass'],
#                                           12, 'ms', 'cs')
#             session['username'] = request.form['username']
#             return redirect(url_for('index'))
#
#         # if existing_user is None:
#         #     # hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
#         #     users.insert({'name': request.form['username'], 'password': hashpass})
#         #     session['username'] = request.form['username']
#         #     return redirect(url_for('index'))
#
#         return 'That username already exists!'
#
#     return render_template('register.html')


if __name__ == '__main__':
    mongo_setup.global_init()  # Connect to the db

    app.secret_key = 'mysecret'
    app.run(debug=True)
