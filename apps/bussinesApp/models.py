#-*- coding:utf-8 -*-
#!/usr/bin/env python
from datetime import datetime
from apps import db


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(80),nullable=False)
    body = db.Column(db.Text,nullable=False)
    pub_date = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)

    category_id = db.Column(db.Integer,db.ForeignKey('category.id'),nullable=False)
