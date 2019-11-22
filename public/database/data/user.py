import mongoengine

# This is an object file for creating the Document structure

class User(mongoengine.Document):
    name = mongoengine.StringField(required=True)
    email = mongoengine.StringField(required=True)
    password = mongoengine.StringField(required=True)
    age = mongoengine.IntField(required=True, min=16)

    educ = mongoengine.StringField(required=True)
    major = mongoengine.StringField(required=True)

    preferences = mongoengine.DictField(required=True)
    weight_sum = mongoengine.IntField(required=True, default=0)

    meta = {
        'db_alias': 'core',
        'collection': 'user' 
    }