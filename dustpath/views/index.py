from flask import (Blueprint,
                   Flask,
                   redirect,
                   render_template,
                   url_for,
                   current_app,
                   redirect)
from .. import models
import datetime
import mongoengine as me
import pathlib

module = Blueprint('main', __name__, url_prefix='/')

@module.route('/')
def index():
    return render_template('main/index.html')
