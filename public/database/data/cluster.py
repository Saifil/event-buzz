import mongoengine

class Cluster(mongoengine.Document):

    # "title", "description", "category", "location", "image_url", "related_link", "st_date", "end_date",
    # "st_time", "end_time"
    number = mongoengine.IntField(required=True)
    name = mongoengine.StringField(required=True)
    event_count = mongoengine.IntField(required=True)

    meta = {
        'db_alias': 'core',
        'collection': 'cluster'
    }
