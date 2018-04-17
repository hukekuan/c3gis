#-*- coding:utf-8 -*-
#!/usr/bin/env python

import json
from datetime import datetime
from uuid import uuid4

from flask import redirect
from flask import request
from flask_login import login_url
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature, text_type
from apps import app, db, loginManager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

users_roles = db.Table('users_roles',
    db.Column('user_id',db.String(45),db.ForeignKey('sys_user.userid')),
    db.Column('role_id', db.String(45), db.ForeignKey('sys_role.roleid')))

roles_menus = db.Table('roles_menus',
    db.Column('role_id',db.String(45),db.ForeignKey('sys_role.roleid')),
    db.Column('menu_id', db.String(45), db.ForeignKey('sys_menu.menuid')))

#====================================user start==========================================#
class User(UserMixin,db.Model):
    __tablename__='sys_user'
    userid = db.Column(db.String(64),primary_key=True)
    username = db.Column(db.String(64),unique=True)
    email = db.Column(db.String(120),unique=True)
    password_hash = db.Column(db.String(128))
    sortednum = db.Column(db.Integer, nullable=False, default=0)
    generate_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    update_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # many to many: user <==> roles
    roles = db.relationship(
        'Role',
        secondary = 'users_roles',
        backref = db.backref('sys_user', lazy='dynamic')
    )
    # one to many: User ==> Post
    posts = db.relationship(
        'Post',
        back_populates='user'
    )

    def __init__(self,username,email,password,sortednum):
        self.userid = str(uuid4())
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)

        self.sortednum = sortednum
        self.generate_date = datetime.utcnow()
        self.update_date = datetime.utcnow()

        # 为用户设置默认角色
        default = Role.query.filter_by(rolename="default").one()
        self.roles.append(default)

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
            return obj.__str__()
        result = obj.__dict__
        if 'generate_date' in result.keys():
            result['generate_date'] = result['generate_date'].strftime('%Y-%m-%d-%H %H:%M:%S')
        if 'update_date' in result.keys():
            result['update_date'] = result['update_date'].strftime('%Y-%m-%d-%H %H:%M:%S')
        if 'password_hash' in result.keys():
            del result['password_hash']
        if '_sa_instance_state' in result.keys():
            del result['_sa_instance_state']
        return result

@loginManager.user_loader
def load_user(userid):
    return User.query.get(userid)

@loginManager.unauthorized_handler
def unauthorized():
    return redirect(login_url('login', request.url))
#====================================user end=======================================#


#====================================role satrt=====================================#
class Role(db.Model):
    __tablename__='sys_role'
    roleid = db.Column(db.String(45), primary_key=True)
    rolename = db.Column(db.String(255), unique=True)
    sortednum = db.Column(db.Integer, nullable=False, default=0)
    generate_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    update_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    description = db.Column(db.String(255))

    menus = db.relationship(
        'Menu',
        secondary='roles_menus',
        backref=db.backref('sys_role', lazy='dynamic')
    )

    def __init__(self, rolename, description, sortednum):
        self.roleid = str(uuid4())
        self.rolename = rolename
        self.description = description
        self.sortednum = sortednum
        self.generate_date = datetime.utcnow()
        self.update_date = datetime.utcnow()
    def __repr__(self):
        return "<Model Role `{}`>".format(self.rolename)

    def save(self):
        db.session.add(self)
        db.session.commit()

class RoleEncoder(json.JSONEncoder):
    def default(self,obj):
        if not isinstance(obj,Role):
            return obj.__str__()
        result = obj.__dict__
        if 'generate_date' in result.keys():
            result['generate_date'] = result['generate_date'].strftime('%Y-%m-%d-%H %H:%M:%S')
        if 'update_date' in result.keys():
            result['update_date'] = result['update_date'].strftime('%Y-%m-%d-%H %H:%M:%S')
        return result

class TableResult:
    def __init__(self,count,data,code,msg):
        self.count = count
        self.data = data
        self.code = code
        self.msg = msg
class TableResultEncoder(json.JSONEncoder):
    def default(self,obj):
        return obj.__dict__
#====================================role end=======================================#






#====================================menu satrt=====================================#
class Menu(db.Model):
    __tablename__='sys_menu'
    menuid = db.Column(db.String(45), primary_key=True)
    parentid = db.Column(db.String(45))
    menuname = db.Column(db.String(255))
    href = db.Column(db.String(255))
    target = db.Column(db.String(255))
    icon = db.Column(db.String(255))
    menutype = db.Column(db.Integer, nullable=False, default=0)
    isshow = db.Column(db.Boolean, default=True)
    isfront = db.Column(db.Boolean, default=True)
    sortednum = db.Column(db.Integer, nullable=False, default=0)
    generate_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    update_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self,parentid,menuname,href,target,icon,menutype,isshow,isfront,sortednum):
        self.menuid = str(uuid4())
        self.parentid = parentid if parentid else '0'
        self.menuname = menuname
        self.href = href
        self.target = target
        self.icon = icon
        self.menutype = menutype
        self.isshow = isshow
        self.isfront = isfront
        self.sortednum = sortednum
        self.generate_date = datetime.utcnow()
        self.update_date = datetime.utcnow()

    def save(self):
        db.session.add(self)
        db.session.commit()

class MenuEncoder(json.JSONEncoder):
    def default(self,obj):
        if not isinstance(obj,Menu):
            return obj.__str__()
        result = obj.__dict__
        if 'generate_date' in result.keys():
            result['generate_date'] = result['generate_date'].strftime('%Y-%m-%d-%H %H:%M:%S')
        if 'update_date' in result.keys():
            result['update_date'] = result['update_date'].strftime('%Y-%m-%d-%H %H:%M:%S')
        return result
#====================================menu end=====================================#