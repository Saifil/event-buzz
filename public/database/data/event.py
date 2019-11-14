import mongoengine

class Event(mongoengine.Document):

    # "title", "description", "category", "location", "image_url", "related_link", "st_date", "end_date",
    # "st_time", "end_time"
    title = mongoengine.StringField(required=True)
    description = mongoengine.StringField()
    category = mongoengine.StringField(default="Unknown")
    location = mongoengine.StringField(required=True)
    image_url = mongoengine.StringField()
    related_link = mongoengine.StringField()
    st_date = mongoengine.DateTimeField(required=True)
    end_date = mongoengine.DateTimeField()
    st_time = mongoengine.IntField(required=True)
    end_time = mongoengine.IntField()
    cluster_number = mongoengine.IntField(default=0)

    meta = {
        'db_alias': 'core',
        'collection': 'event'
    }
