from flask_mongoengine import MongoEngine
from .users import User, AuthSecret 
from .maps import CircleMap

db = MongoEngine()

__all__ = [
    User, CircleMap
]


def init_db(app):
    db.init_app(app)
    
def init_mongoengine(settings):
    import mongoengine as me

    dbname = settings.get("MONGODB_DB")
    host = settings.get("MONGODB_HOST", "localhost")
    port = int(settings.get("MONGODB_PORT", "27017"))
    username = settings.get("MONGODB_USERNAME", "")
    password = settings.get("MONGODB_PASSWORD", "")
    me.connect(db=dbname, host=host, port=port, username=username, password=password)
