from database.data.user import User
from database.data.event import Event

def create_new_user(first_name, last_name, email):
    usr = User()
    usr.first_name = first_name
    usr.last_name = last_name
    usr.email = email

    usr.save()
    return usr

def create_multiple_users(user_document_list):
    usrs = User.objects().insert(user_document_list)
    return usrs


def get_user_info(email):
    usr = User.objects().filter(email=email).first()
    return usr

def insert_events(event_document_list):
    ret = Event.objects().insert(event_document_list)
    return ret

def get_all_event_data():
    events = Event.objects()
    return events
