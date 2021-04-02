from flask import g, config, session, redirect, url_for, request, current_app
from flask_login import current_user, login_user
from authlib.integrations.flask_client import OAuth
from flask_principal import identity_changed, Identity
import loginpass

from . import models
import mongoengine as me

import datetime


def fetch_token(name):
    token = models.OAuth2Token.objects(
        name=name,
        user=current_user._get_current_object()
        ).first()
    return token.to_dict()


def update_token(name, token):
    item = models.OAuth2Token(
        name=name,
        user=current_user._get_current_object()
        ).first()
    item.token_type = token.get('token_type', 'Bearer')
    item.access_token = token.get('access_token')
    item.refresh_token = token.get('refresh_token')
    item.expires = datetime.datetime.utcfromtimestamp(token.get('expires_at'))
    item.save()
    return item


oauth2_client = OAuth()


def handle_authorize_oauth2(remote, token, user_info):

    if not user_info:
        return redirect(url_for('accounts.login'))

    user = models.User.objects(me.Q(email=user_info.get('email'))).first()
    if not user:
        if remote.name == 'google':
            user = google_register(user_info)
        elif remote.name == 'facebook':
            user = facebook_register(user_info)

    login_user(user)
    identity_changed.send(
            current_app._get_current_object(),
            identity=Identity(str(user.id)))


    if token:
        oauth2token = models.OAuth2Token(
                name=remote.name,
                user=user,
                access_token=token.get('access_token'),
                token_type=token.get('token_type'),
                refresh_token=token.get('refresh_token', None),
                expires=datetime.datetime.utcfromtimestamp(
                        token.get('expires_in'))
                )
        oauth2token.save()

    next_uri = session.get('next', None)
    if next_uri:
        session.pop('next')
        return redirect(next_uri)
    return redirect(url_for('dashboard.index'))


def google_register(user_info):
    user = models.User(
        picture_url=user_info.get('picture'),
        email=user_info.get('email'),
        firstname=user_info.get('given_name'),
        lastname=user_info.get('family_name'),
        active=True,)
    user.save()

    return user


def facebook_register(user_info):
    user = models.User(
        picture_url='http://graph.facebook.com/'+user_info.get('sub')+'/picture?type=large',
        email=user_info.get('email'),
        firstname=user_info.get('given_name'),
        lastname=user_info.get('family_name'),
        active=True)
    user.save()

    return user


def init_oauth(app):
    oauth2_client.init_app(app,
                           fetch_token=fetch_token,
                           update_token=update_token)
    backends = [loginpass.Google, loginpass.Facebook]
    loginpass_bp = loginpass.create_flask_blueprint(
            backends,
            oauth2_client,
            handle_authorize_oauth2)
    app.register_blueprint(loginpass_bp)
