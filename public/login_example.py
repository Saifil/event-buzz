from flask import Flask, render_template, url_for, request, session, redirect, jsonify
from flask_pymongo import PyMongo

import database.data.mongo_setup as mongo_setup
import database.services.data_service as svc

import json
import random
import operator
import user_calendar as ucal

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'eventbuzz'
app.config['MONGO_URI'] = 'mongodb://127.0.0.1:27017/eventbuzz'

mongo = PyMongo(app)

NUM_CLUSTER = 50
NUM_EVENTS_DISPLAY = 50


@app.route('/')
def index():
    # if 'email' in session:
    # redirect user to his event page
    # TODO: display user name on event page | NOT IMP
    # return redirect(url_for('events'))
    # return 'You are logged in as ' + session['email']

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
            # TODO: display credentials wrong
            return render_template('login.html')
    return render_template('login.html')


@app.route('/events', methods=['POST', 'GET'])
def events():
    # event_list = svc.get_all_event_data()
    event_list = []

    usr_email = session['email']
    print(usr_email)
    user = svc.get_user_pref(usr_email)
    pref = user.preferences
    weight_sum = user.weight_sum

    # print(type(pref))

    pref_dict = {}
    is_one = True  # check if all are one
    for key in pref:
        if pref[key] != 0:
            if pref[key] != 1:
                is_one = False
            pref_dict[key] = pref[key]

    print(pref_dict)

    pref_sorted = sorted(pref_dict.items(), key=operator.itemgetter(1))
    if not is_one:  # not all are one
        pref_sorted.reverse()
    pref = dict(pref_sorted)

    for key in pref:
        # if pref[key] != 0:
        cluster_num_events = pref[key] * NUM_EVENTS_DISPLAY // weight_sum
        event_list += list(svc.get_event_by_cluster_limit(key, cluster_num_events))

    # Shuffled all the events
    # random.shuffle(event_list)

    return render_template('event_data.html', data=event_list)

@app.route('/all_events', methods=['POST', 'GET'])
def all_events():
    event_list = svc.get_all_event_data()
    # event_list = []
    #
    # usr_email = session['email']
    # print(usr_email)
    # user = svc.get_user_pref(usr_email)
    # pref = user.preferences
    # weight_sum = user.weight_sum
    #
    # # print(type(pref))
    #
    # pref_dict = {}
    # is_one = True # check if all are one
    # for key in pref:
    #     if pref[key] != 0:
    #         if pref[key] != 1:
    #             is_one = False
    #         pref_dict[key] = pref[key]
    #
    # print(pref_dict)
    #
    # pref_sorted = sorted(pref_dict.items(), key=operator.itemgetter(1))
    # if not is_one: # not all are one
    #     pref_sorted.reverse()
    # pref = dict(pref_sorted)
    #
    # for key in pref:
    #     # if pref[key] != 0:
    #     cluster_num_events = pref[key] * NUM_EVENTS_DISPLAY // weight_sum
    #     event_list += list(svc.get_event_by_cluster_limit(key, cluster_num_events))
    #
    # # Shuffled all the events
    # random.shuffle(event_list)

    return render_template('all_event_data.html', data=event_list)


@app.route('/profile', methods=['POST', 'GET'])
def profile():
    usr_email = session['email']
    user = svc.get_user_pref(usr_email)
    print(user.name)
    print("JHIHIIHIIHIHHIHIIHIH")

    return render_template('profile.html', data=user)




@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        age = request.form['age']
        educ = request.form['educ']
        major = request.form['major']
        cluster_list = request.form.getlist("cluster_keys")
        # print(cluster_list) # to int
        preferences = {}
        for i in range(NUM_CLUSTER):
            preferences[str(i)] = 0

        for cluster in cluster_list:
            preferences[cluster] += 1

        print(f"Name: {name}")

        users = svc.get_user_info(email, password)
        if users is None:
            new_usr = svc.create_new_user(name, email, password, age, educ, major, preferences, len(cluster_list))
            session['email'] = new_usr.email
            return redirect(url_for('index'))
            # return render_template('index.html')

        # if existing_user is None:
        #     # hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
        #     users.insert({'name': request.form['username'], 'password': hashpass})
        #     session['username'] = request.form['username']
        #     return redirect(url_for('index'))

        return 'That username already exists!'

    clstrs = svc.get_all_clusters()

    return render_template('signup.html', data=clstrs)
    # return render_template('register.html')


@app.route('/background_process_test', methods=['POST', 'GET'])
def background_process_test():
    if request.method == 'POST':
        cluster = request.form['cluster']
        print(cluster)
        ret = svc.update_user_preference(session['email'], cluster)

        # TODO: add the event to the calender
        # email = 'myubereats.free07@gmail.com'
        # service = ucal.authenticate_user(email)
        # calendar_id, time_zone = ucal.get_calendar_id_and_timezone(service)

        return jsonify({'status': 'True'})
    return jsonify({'status': 'False'})


@app.route('/user_calendar')
def user_calendar():
    data = {'email': 'myubereats.free07@gmail.com'}
    return render_template('user_calendar.html', data=data)
    # email = 'myubereats.free07@gmail.com'
    # service = ucal.authenticate_user(email)
    # calendar_id, time_zone = ucal.get_calendar_id_and_timezone(service)
    # # print(calendar_id)
    #
    # return calendar_id


@app.route('/android', methods=['POST', 'GET'])
def android():
    event_list = svc.get_all_event_data()
    """
    long time = 1566518400000L;
    SimpleDateFormat sdf = new SimpleDateFormat();
    sdf.setTimeZone(TimeZone.getTimeZone("UTC"));
    System.out.println(sdf.format(new Date(time)));
    """
    return event_list.to_json()

    # return json.dumps(event_list[0], default=json_util.default)
    # return json.dumps(event_list)


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


"""
@Android Server functions
"""


@app.route('/login_android', methods=['POST'])
def login_android():
    if request.method == 'POST':
        # TODO: protect from injection attack
        email = request.form['email']
        password = request.form['password']

        user = svc.get_user_info(email, password)
        if user is not None:
            response = {"status": "true", "email": user.email, "name": user.name, "age": user.age}
            return json.dumps(response)
        else:
            response = {"status": "false"}
            return json.dumps(response)


if __name__ == '__main__':
    mongo_setup.global_init()  # Connect to the db

    app.secret_key = 'mysecret'
    app.run(debug=True)
