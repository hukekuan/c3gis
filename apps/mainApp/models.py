#-*- coding:utf-8 -*-
#!/usr/bin/env python

import json
from uuid import uuid4

from flask import redirect
from flask import request
from flask_login import login_url
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature, text_type
from apps import app, db, loginManager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin,db.Model):
    __tablename__='sys_user'
    userid = db.Column(db.String(64),primary_key=True)
    username = db.Column(db.String(64),unique=True)
    email = db.Column(db.String(120),unique=True)
    password_hash = db.Column(db.String(128))

    def __init__(self,username,email,password):
        self.userid = str(uuid4())
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def get_id(self):
        try:
            return text_type(self.userid)
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expiration)
        return s.dumps({'id': self.userid})

    def save(self):
        db.session.add(self)
        db.session.commit()
        pass

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        return User.query.get(str(data['id']))

    def __repr__(self):
        return '<User %r>' % self.username

class UserEncoder(json.JSONEncoder):
    def default(self,obj):
        if not isinstance(obj,User):
            return obj.__str__
        result = obj.__dict__
        del result['password_hash']
        del result['_sa_instance_state']
        return obj.__dict__

@loginManager.user_loader
def load_user(userid):
    return User.query.get(userid)

@loginManager.unauthorized_handler
def unauthorized():
    return redirect(login_url('login', request.url))