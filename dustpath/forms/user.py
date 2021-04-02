from flask_wtf import FlaskForm
from wtforms import fields
# from wtforms.fields import html5
from wtforms import validators

class ProfileForm(FlaskForm):
    firstname = fields.StringField('ชื่อ',
                                 validators=[validators.Length(min=1)])
    lastname = fields.StringField('นามสกุล',
                                validators=[validators.Length(min=1)])