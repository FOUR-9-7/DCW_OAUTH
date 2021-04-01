from flask import (Blueprint,
                   render_template,
                   redirect,
                   url_for,
                   request,
                   jsonify
                   )
import json, datetime
from flask_login import login_required
from .. import models

module = Blueprint('maps', __name__, url_prefix='/maps')

@module.route('/')
def index():
    maps = models.CircleMap.objects()
    return render_template('maps/index.html',
                            maps=maps,)

@module.route('/record', methods=['GET', 'POST'])
def record():
    
    center = [7.0065949668769205, 100.49891880632555] # lat, long
    zoom = 10
    
    if request.method == 'POST':
        data = request.json
        if data:
            circle_map = models.CircleMap(center=data['center'], radius=data['radius'])
            circle_map.save()
    return render_template('maps/record.html',
                           zoom=zoom,
                           center=center,)