from flask import (Blueprint, render_template,
                   url_for, redirect, request)
from flask_login import (login_required)
from dustpath import models
from dustpath.forms import ProfileForm

module = Blueprint('users', __name__, url_prefix='/users')

@module.route('/record', methods=['GET', 'POST'])
def all_profile():
    user = models.User.objects().first()
    return render_template('users/profile.html', user=user)

@module.route('/record', methods=['GET', 'POST'])
def record():
    user_id = request.args.get('user_id')
    if user_id:
        user = models.User.objects.get(id=user_id)
        form = ProfileForm(obj=user)
    else:
        user = models.User()
        form = ProfileForm()
        
    if not form.validate_on_submit():
        return render_template('users/record.html', user=user,
                                                    form=form,)
    
    form.populate_obj(user)
    user.save()

    return redirect(url_for('users.record', user=user))