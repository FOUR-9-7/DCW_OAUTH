import mongoengine as me
import datetime
from flask_login import UserMixin

class AuthSecret(me.Document):
    meta = {'collection': 'auth_secrets'}
    user = me.ReferenceField('User', dbref=True, required=True)
    secret = me.StringField(required=True)
    create_at = me.DateTimeField(
            required=True,
            default=datetime.datetime.now)
    expire_at = me.DateTimeField(
            required=True,
            default=datetime.datetime.now() + datetime.timedelta(days=1))

class User(me.Document, UserMixin):
    meta = {'collection': 'users'}

    firstname = me.StringField(required=True)
    lastname = me.StringField(required=True)
