import mongoengine

class Book(mongoengine.EmbeddedDocument):
    book_id = mongoengine.ObjectIdField()
    book_name = mongoengine.StringField(required=True)
    author = mongoengine.StringField(required=True)
    times_issued = mongoengine.IntField(default=0)
    average_rating = mongoengine.FloatField(required=True, min=0.0, max=5.0)