from database.data.user import User
from database.data.event import Event
from database.data.cluster import Cluster


def create_new_user(name, email, password, age, educ, major, preferences, weight_sum):
    usr = User()

    usr.name = name
    usr.email = email
    usr.password = password
    usr.age = age
    usr.educ = educ
    usr.major = major
    usr.preferences = preferences
    usr.weight_sum = weight_sum

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


def get_cluster_counts(cluster=0):
    cluster_count = Event.objects(cluster_number=cluster).count()
    return cluster_count


def create_new_cluster(number, name, event_count):
    clsrt = Cluster()
    clsrt.number = number
    clsrt.name = name
    clsrt.event_count = event_count

    clsrt.save()
    return clsrt


def get_all_clusters():
    clstrs = Cluster.objects().filter()
    return clstrs


def get_user_pref(email):
    pref = User.objects().filter(email=email).first()
    return pref


def get_event_by_cluster_limit(cluster=0, limit=10):
    events = Event.objects.filter(cluster_number=cluster).aggregate(
        {'$group': {'originalId': {'$first': '$_id'},
                    '_id': '$title',
                    'description': {'$first': '$description'},
                    'category': {'$first': '$category'},
                    'location': {'$first': '$location'},
                    'image_url': {'$first': '$image_url'},
                    'related_link': {'$first': '$related_link'},
                    'st_date': {'$first': '$st_date'},
                    'end_date': {'$first': '$end_date'},
                    'st_time': {'$first': '$st_time'},
                    'cluster_number': {'$first': '$cluster_number'},
                    }
         },
        {'$project': {'_id': '$originalId',
                      'title': "$_id",
                      'description': '$description',
                      'category': '$category',
                      'location': '$location',
                      'image_url': '$image_url',
                      'related_link': '$related_link',
                      'st_date': '$st_date',
                      'end_date': '$end_date',
                      'st_time': '$st_time',
                      'cluster_number': '$cluster_number',
                      }
         },
        {'$limit': limit}
    )
    return events


def update_user_preference(email, cluster=0, inc_value=1):
    field = 'inc__preferences__' + str(cluster)
    uptd = User.objects(email=email).update(**{field: inc_value})
    return uptd
