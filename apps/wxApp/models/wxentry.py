#-*- coding:utf-8 -*-
#!/usr/bin/env python

import time
import hashlib
import json
import random
import string
from datetime import datetime
from operator import and_
from uuid import uuid4

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
    id = db.Column(db.String(45), primary_key=True)
    appid = db.Column(db.String(45), nullable=True)
    token = db.Column(db.String(500), nullable=True)
    type = db.Column(db.Integer, nullable=False, default=0)
    updatedate = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __init__(self, appid, token, type):
        self.id = str(uuid4())
        self.appid = appid
        self.token = token
        self.type = type
        self.updatedate = datetime.now()
    def save(self):
        db.session.add(self)
        db.session.commit()
    def update(self):
        timeOffset = (datetime.now() - self.updatedate).seconds
        if timeOffset < 7000:
            return
        if self.type == 0:
            queryApp = UserEntry.query.filter_by(appid = self.appid).first()
            if queryApp:
                accessToken = AccessToken.QueryAccessTokeByRemoteServer(self.appid,queryApp.appsecret)
                if accessToken:
                    self.token = accessToken
                    self.updatedate = datetime.now()
        elif self.type == 1:
            queryAccessToken = AccessToken.query.filter(and_(AccessToken.appid == self.appid, AccessToken.type == 0)).first()
            if queryAccessToken:
                jsapiToken = AccessToken.QueryJSAPITokeByRemoteServer(queryAccessToken.token)
                self.token = jsapiToken
                self.updatedate = datetime.now()

        db.session.commit()

    @staticmethod
    def CreateToken(appid, appsecret):
        accessToken = AccessToken.QueryAccessTokeByRemoteServer(appid, appsecret)
        if accessToken:
            newToken = AccessToken(appid, accessToken, 0)
            newToken.save()
            jsapiToken = AccessToken.QueryJSAPITokeByRemoteServer(accessToken)
            if jsapiToken:
                newToken = AccessToken(appid, jsapiToken, 1)
                newToken.save()

    @staticmethod
    def QueryAccessTokeByRemoteServer(appid, appsecret):
        appParams = {'grant_type': 'client_credential', 'appid': appid, 'secret': appsecret}
        tokenRequest = requests.get('https://api.weixin.qq.com/cgi-bin/token', params=appParams)
        tokenResult = tokenRequest.json()
        if tokenResult and 'access_token' in tokenResult.keys():
            accessToken = tokenResult['access_token']
        return accessToken

    @staticmethod
    def QueryJSAPITokeByRemoteServer(accessToken):
        appParams = {'type': 'jsapi', 'access_token': accessToken}
        tokenRequest = requests.get('https://api.weixin.qq.com/cgi-bin/ticket/getticket', params=appParams)
        tokenResult = tokenRequest.json()
        if tokenResult and 'ticket' in tokenResult.keys():
            accessToken = tokenResult['ticket']
        return accessToken

class AccessTokenEncoder(json.JSONEncoder):
    def default(self, obj):
        if not isinstance(obj, AccessToken):
            return obj.__str__()
        result = obj.__dict__
        return result

class Sign:
    def __init__(self, jsapi_ticket, url):
        self.ret = {
            'nonceStr': self.__create_nonce_str(),
            'jsapi_ticket': jsapi_ticket,
            'timestamp': self.__create_timestamp(),
            'url': url
        }

    def __create_nonce_str(self):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))

    def __create_timestamp(self):
        return int(time.time())

    def sign(self):
        string = '&'.join(['%s=%s' % (key.lower(), self.ret[key]) for key in sorted(self.ret)])
        self.ret['signature'] = hashlib.sha1(string).hexdigest()
        return self.ret