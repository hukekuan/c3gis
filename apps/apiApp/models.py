#-*- coding:utf-8 -*-
#!/usr/bin/env python
from sqlalchemy import Integer
from sqlalchemy.dialects.postgresql import JSONB, ARRAY

from apps import db

class Chart(db.Model):
    id = db.Column(db.String(200), primary_key=True,unique=True)
    name = db.Column(db.String(200))
    description = db.Column(db.Text)
    chart = db.Column(db.JSON)

    def __init__(self,id,name,description,chart):
        self.id = id
        self.name = name
        self.description = description
        self.chart = chart

class Test(db.Model):
    id = db.Column(db.String(200), primary_key=True,unique=True)
    name = db.Column(db.String(200))
    description = db.Column(db.Text)
    chart = db.Column(JSONB)

    def __init__(self,id,name,description,chart):
        self.id = id
        self.name = name
        self.description = description
        self.chart = chart

class Test1(db.Model):
    id = db.Column(db.String(200), primary_key=True,unique=True)
    name = db.Column(db.String(200))
    description = db.Column(db.Text)
    chart = db.Column(JSONB)
    values = db.Column(ARRAY(Integer))

    def __init__(self,id,name,description,chart):
        self.id = id
        self.name = name
        self.description = description
        self.chart = chart