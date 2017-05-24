#-*- coding:utf-8 -*-
#!/usr/bin/env python
# import time
# import datetime
# from apps import cache
# import requests
# from apps import db, app
#
#
# class Token(db.Model):
#     __tablename__ ='sys_token'
#     id = db.Column(db.Integer, primary_key=True,autoincrement=True)
#     tokenname = db.Column(db.String(100),index=True)
#     tokenvalue = db.Column(db.String(600))
#     refreshvalue = db.Column(db.String(600))
#     tokentime  = db.Column(db.BIGINT)
#
#     def __init__(self,tokenname,tokenvalue,refreshvalue,tokentime):
#         self.tokenname = tokenname
#         self.tokenvalue = tokenvalue
#         self.refreshvalue = refreshvalue
#         self.tokentime = tokentime
#
#     def validChecked(self):
#         if self.tokenvalue is None or self.tokentime is None:
#             return False
#         oldDateTime = timeStamp2datetime(self.tokentime)
#         nowDateTime = datetime.datetime.now()
#         if (nowDateTime - oldDateTime).seconds >= 7100:
#             return False
#         return True
#     def updateVale(self):
#         if self.tokenname == 'access':
#             urlStr = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}'\
#                 .format(app.config.get('APPID'),app.config.get('APPSECRET'))
#             r = requests.get(url=urlStr)
#             if r is not None:
#                 queryResult = r.json()
#                 if queryResult.has_key('access_token'):
#                     self.tokenvalue = queryResult['access_token']
#                     self.tokentime = datetime2timeStamp(datetime.datetime.now())
#                     db.session().commit()
#                 elif queryResult.has_key('errmsg'):
#                     raise Exception(queryResult['errmsg'])
#             else:
#                 raise Exception('token acquisition failed')
#         elif self.tokenname == 'ticket':
#             accessToken = Token.query.filter_by(tokenname='access').first()
#             if not accessToken.validChecked():
#                 accessToken = accessToken.updateVale()
#
#             urlStr = 'https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token={}&type=jsapi'.format(accessToken.tokenvalue)
#             r = requests.get(url=urlStr)
#             if r is not None:
#                 queryResult = r.json()
#                 if queryResult.has_key('ticket'):
#                     self.tokenvalue = queryResult['ticket']
#                     self.tokentime = datetime2timeStamp(datetime.datetime.now())
#                     db.session().commit()
#                 elif queryResult.has_key('errmsg'):
#                     raise Exception(queryResult['errmsg'])
#             else:
#                 raise Exception('token acquisition failed')
#         return self
#
#     def __repr__(self):
#         return '<Token %r>' % self.tokenname
#
#
# class PageToken(db.Model):
#     __tablename__ = 'sys_pagetoken'
#     id = db.Column(db.Integer, primary_key=True,autoincrement=True)
#     openid = db.Column(db.String(100),index=True)
#     tokenvalue = db.Column(db.String(600))
#     refreshvalue = db.Column(db.String(600))
#     scope = db.Column(db.String(600))
#     tokentime = db.Column(db.BIGINT)
#
#     def __init__(self,openid,tokenvalue,refreshvalue,scope,tokentime):
#         self.openid = openid
#         self.tokenvalue = tokenvalue
#         self.refreshvalue = refreshvalue
#         self.scope = scope
#         self.tokentime = tokentime
#
#     def validChecked(self):
#         if self.tokenvalue is None or self.tokentime is None:
#             return False
#         oldDateTime = timeStamp2datetime(self.tokentime)
#         nowDateTime = datetime.datetime.now()
#         if (nowDateTime - oldDateTime).seconds >= 7100:
#             return False
#         return True
#
#     def updateVale(self,code):
#         urlStr = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid={}&secret={}&code={}&grant_type=authorization_code'\
#             .format(app.config.get('APPID'),app.config.get('APPSECRET'),code)
#         r = requests.get(url=urlStr)
#         if r is not None:
#             queryResult = r.json()
#             if queryResult.has_key('access_token'):
#                 self.tokenvalue = queryResult['access_token']
#                 self.refreshvalue = queryResult['refresh_token']
#                 self.scope = queryResult['scope']
#                 self.tokentime = datetime2timeStamp(datetime.datetime.now())
#                 db.session().commit()
#             elif queryResult.has_key('errmsg'):
#                 raise Exception(queryResult['errmsg'])
#         else:
#             raise Exception('page token acquisition failed')
#
#         return self
#
#     @classmethod
#     def CreatePageToken(cls,code):
#         urlStr = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid={}&secret={}&code={}&grant_type=authorization_code' \
#             .format(app.config.get('APPID'), app.config.get('APPSECRET'), code)
#         r = requests.get(url=urlStr)
#         if r is not None:
#             queryResult = r.json()
#             if queryResult.has_key('access_token'):
#                 openid = queryResult['openid']
#                 pageToken = PageToken.query.filter_by(openid=openid).first()
#                 if pageToken is None:
#                     pageToken = PageToken(
#                         openid,
#                         queryResult['access_token'],
#                         queryResult['refresh_token'],
#                         queryResult['scope'],
#                         datetime2timeStamp(datetime.datetime.now()))
#                     db.session.add(pageToken)
#                 else:
#                     pageToken.tokenvalue = queryResult['access_token']
#                     pageToken.refreshvalue = queryResult['refresh_token']
#                     pageToken.scope = queryResult['scope']
#                     pageToken.tokentime = datetime2timeStamp(datetime.datetime.now())
#
#                 db.session.commit()
#
#     def __repr__(self):
#         return '<PageToken %r>' % self.openid
#
#
#
#
# def datetime2timeStamp(rawDatetime):
#     if not isinstance(rawDatetime,datetime.datetime):
#         raise ValueError('变量类型错误')
#     return int(time.mktime(rawDatetime.timetuple()))
#
# def timeStamp2datetime(timestap):
#     if not isinstance(timestap,(long,int)):
#         raise ValueError('变量类型错误')
#
#     timeArray = time.localtime(timestap)
#     timeStr = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
#     resultDateTime = datetime.datetime.strptime(timeStr,"%Y-%m-%d %H:%M:%S")
#     return resultDateTime
#
# def getAccess():
#     accessToken = cache.get('access')
#     if accessToken is None:
#         accessToken = Token.query.filter_by(tokenname='access').first()
#         if not accessToken.validChecked():
#             accessToken = accessToken.updateVale()
#         cache.set('access', accessToken, timeout=120 * 60)
#     elif not accessToken.validChecked():
#         accessToken = accessToken.updateVale()
#         cache.set('access', accessToken, timeout=120 * 60)
#     return accessToken
#
# def getTicket():
#     ticketToken = cache.get('ticket')
#     if ticketToken is None:
#         ticketToken = Token.query.filter_by(tokenname='ticket').first()
#         if not ticketToken.validChecked():
#             ticketToken = ticketToken.updateVale()
#         cache.set('ticket', ticketToken, timeout=120 * 60)
#     elif not ticketToken.validChecked():
#         ticketToken = ticketToken.updateVale()
#         cache.set('ticket', ticketToken, timeout=120 * 60)
#     return ticketToken