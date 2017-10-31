#-*- coding:utf-8 -*-
#!/usr/bin/env python

import time
import random
import string
import hashlib
from xml.etree import ElementTree

from apps import app
import requests


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


class WXToken():
    def __init__(self):
        self.type = None
        self.value = None

    def tokeninit(self,tokenType):
        if tokenType:
            urlStr = app.config['TOKENURL'].format(tokenType)
            r = requests.get(url=urlStr)
            if r and r.content:
                queryResult = r.json()
                self.value = queryResult['tokenValue']
                self.type = tokenType


class Msg():
    def __init__(self,xmlData):
        self.ToUserName = xmlData.find('ToUserName').text
        self.FromUserName = xmlData.find('FromUserName').text
        self.CreateTime = xmlData.find('CreateTime').text
        self.MsgType = xmlData.find('MsgType').text
        self.MsgId = xmlData.find('MsgId').text

class TextMsg(Msg):
    def __init__(self, xmlData):
        Msg.__init__(self, xmlData)
        self.Content = xmlData.find('Content').text.encode("utf-8")

class ImageMsg(Msg):
    def __init__(self, xmlData):
        Msg.__init__(self, xmlData)
        self.PicUrl = xmlData.find('PicUrl').text
        self.MediaId = xmlData.find('MediaId').text

def parse_xml(webData):
    if len(webData) <= 0:
        return None
    xmlData = ElementTree.fromstring(webData)
    msg_type = xmlData.find('MsgType').text
    if msg_type == 'text':
        return TextMsg(xmlData)
    elif msg_type == 'image':
        return ImageMsg(xmlData)
