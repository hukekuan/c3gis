#-*- coding:utf-8 -*-
#!/usr/bin/env python
from sqlalchemy.dialects.postgresql import JSONB

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