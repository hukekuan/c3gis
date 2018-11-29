#-*- coding:utf-8 -*-
#!/usr/bin/env python
from datetime import datetime
from uuid import uuid4

from geoalchemy2 import Geometry

from apps import db


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.String(45),primary_key=True)
    title = db.Column(db.String(80),nullable=False)
    body = db.Column(db.Text,nullable=False)
    pub_date = db.Column(db.DateTime,nullable=False,default=datetime.now)
    # Set the foreign key for Post
    user_id = db.Column(db.String(45), db.ForeignKey('sys_user.userid'))
    # one to many: user <==> posts
    user = db.relationship(
        'User',
        back_populates='posts')

    def __init__(self):
        self.id=str(uuid4())

    def __repr__(self):
        return '<Model Post `{}`>'.format(self.title)


class GeoCity(db.Model):
    __bind_key__ = 'gisdb'
    __tablename__ = 'geocity'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(80),nullable=False)
    geom = db.Column(Geometry('POLYGON'))