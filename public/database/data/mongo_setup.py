import mongoengine

alias_core = 'core'
db_name = 'eventbuzz'

# Connect to MongoDB database
def global_init():
    mongoengine.register_connection(alias=alias_core, name=db_name)

