#-*- coding:utf-8 -*-
#!/usr/bin/env python
import json
from datetime import datetime
from apps import app, db


class UserEntry(db.Model):
    __tablename__ = 'wx_user'
    userid = db.Column(db.String(45), primary_key=True)
    username = db.Column(db.String(45), nullable=True)
    appid = db.Column(db.String(45), nullable=True)
    appsecret = db.Column(db.String(45), nullable=True)
    apptype = db.Column(db.Integer, nullable=False, default=0)
    sortednum = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self,userid,username,appid,appsecret,apptype,sortednum):
        self.userid = userid
        self.username = username
        self.appid = appid
        self.appsecret = appsecret
        self.apptype = apptype
        self.sortednum = sortednum
    def save(self):
        db.session.add(self)
        db.session.commit()


class UserEntryEncoder(json.JSONEncoder):
    def default(self, obj):
        if not isinstance(obj, UserEntry):
            return obj.__str__()
        result = obj.__dict__
        return result


class AccessToken(db.Model):
    __tablename__ = 'wx_access'
    appid = db.Column(db.String(45), primary_key=True)
    token = db.Column(db.String(500), nullable=True)
    updatedate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self,appid,token):
        self.appid = appid
        self.token = token
        self.updatedate = datetime.utcnow()
    def save(self):
        db.session.add(self)
        db.session.commit()

class AccessTokenEncoder(json.JSONEncoder):
    def default(self, obj):
        if not isinstance(obj, AccessToken):
            return obj.__str__()
        result = obj.__dict__
        return result