import mongoengine
from database.data.book import Book

# This is an object file for creating the Document structure

class User(mongoengine.Document):
    first_name = mongoengine.StringField(required=True)
    last_name = mongoengine.StringField()
    email = mongoengine.StringField(required=True)

    currently_issued_books = mongoengine.EmbeddedDocumentListField(Book)

    meta = {
        'db_alias': 'core',
        'collection': 'user' 
    }