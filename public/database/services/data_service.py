from database.data.user import User
from database.data.event import Event

def create_new_user(name, email, password, age, educ, major):
    usr = User()

    usr.name = name
    usr.email = email
    usr.password = password
    usr.age = age
    usr.educ = educ
    usr.major = major

    usr.save()
    return usr

def create_multiple_users(user_document_list):
    usrs = User.objects().insert(user_document_list)
    return usrs


def get_user_info(email, password):
    usr = User.objects().filter(email=email, password=password).first()
    return usr

def insert_events(event_document_list):
    ret = Event.objects().insert(event_document_list)
    return ret

def get_all_event_data():
    events = Event.objects().filter()

    # TODO: Remove
    # events = Event.objects(image_url__ne="gatech_logo.png")
    return events

def get_events_by_clusters(cluster=0):
    events = Event.objects().filter(cluster_number=cluster)
    return events

def get_unique_descriptions():
    events = Event.objects.distinct('description')
    return events
