import mongoengine as me
import datetime

class CircleMap(me.Document):
    meta = {'collection': 'circle_maps'}

    center = me.GeoPointField(required=True)
    radius = me.IntField(required=True)
