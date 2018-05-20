#-*- coding:utf-8 -*-
#!/usr/bin/env python
import json
from datetime import datetime

import requests

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
    updatedate = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __init__(self,appid,token):
        self.appid = appid
        self.token = token
        self.updatedate = datetime.now()
    def save(self):
        db.session.add(self)
        db.session.commit()
    def update(self):
        timeOffset = (datetime.now() - self.updatedate).seconds
        if timeOffset < 7000:
            return
        queryApp = UserEntry.query.filter_by(appid = self.appid).first()
        if queryApp:
            accessToken = AccessToken.QueryAccessTokeByRemoteServer(self.appid,queryApp.appsecret)
            if accessToken:
                self.token = accessToken
                self.updatedate = datetime.now()
                db.session.commit()

    @staticmethod
    def CreateToken(appid, appsecret):
        accessToken = AccessToken.QueryAccessTokeByRemoteServer(appid, appsecret)
        if accessToken:
            newToken = AccessToken(appid, accessToken)
            newToken.save()
    @staticmethod
    def QueryAccessTokeByRemoteServer(appid, appsecret):
        appParams = {'grant_type': 'client_credential', 'appid': appid, 'secret': appsecret}
        tokenRequest = requests.get('https://api.weixin.qq.com/cgi-bin/token', params=appParams)
        tokenResult = tokenRequest.json()
        if tokenResult and 'access_token' in tokenResult.keys():
            accessToken = tokenResult['access_token']
        return accessToken

class AccessTokenEncoder(json.JSONEncoder):
    def default(self, obj):
        if not isinstance(obj, AccessToken):
            return obj.__str__()
        result = obj.__dict__
        return result