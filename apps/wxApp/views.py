# -*- coding:utf-8 -*-
# !/usr/bin/env python
import importlib
import json
import sys
import time
from operator import and_

from flask_login import login_required

from apps.mainApp.models import TableResult, TableResultEncoder
from apps.wxApp.models.wxentry import UserEntry, UserEntryEncoder, AccessToken, Sign
from apps.wxApp.models.wxmessage import ArticleItem, ArticleMsg
from apps.wxApp.utils import parse_xml

importlib.reload(sys)
from flask import request, render_template, jsonify
from apps import app
from apps.wxApp import wx


@wx.route('/MP_verify_d27KRyv47e80atfj.txt', methods=['GET'])
def jsCheck():
    return app.send_static_file('wx/MP_verify_d27KRyv47e80atfj.txt')


@wx.route('/token', methods=['GET', 'POST'])
def Token():
    if request.method == 'GET' and 'echostr' in request.args.keys():
        result = request.args['echostr']
        return result

    elif request.method == 'POST':
        receiveMsg = parse_xml(request.data)
        if receiveMsg.MsgType == 'event':
            return ''
        articleItem1 = ArticleItem(
            '中乌发动机合作生变？乌克兰地方法院冻结中资股份',
            'http://c3gis-c3gis.stor.sinaapp.com/images/a.jpeg',
            'http://c3gis.applinzi.com')
        articleItem2 = ArticleItem(
            '中国新型无人武直惊艳亮相，优势独特全世界仅3国能造',
            'http://c3gis-c3gis.stor.sinaapp.com/images/a.jpeg',
            'http://c3gis.applinzi.com')
        articleMsg = ArticleMsg(receiveMsg.FromUserName, receiveMsg.ToUserName, [articleItem1, articleItem2])

        return articleMsg.xmlFormat()


@wx.route('/index', methods=['GET'])
def test():
    return render_template('wx/wxindex.html', **locals())


#################################################公众号管理 start#######################################################
@app.route('/wx/entrymanage')
@login_required
def entrymanage():
    return render_template('wx/entrymanage.html', **locals())


@app.route('/wx/pageentries', methods=['GET'])
@login_required
def entrylistBypage():
    page = int(request.args.get('page'))
    limit = int(request.args.get('limit'))
    userPagination = UserEntry.query.order_by(UserEntry.sortednum).paginate(page, limit)
    userlist = userPagination.items
    tableResult = TableResult(
        userPagination.pages * limit,
        json.loads(json.dumps(userlist, cls=UserEntryEncoder)),
        0, ""
    )
    return json.dumps(tableResult, cls=TableResultEncoder)


@app.route('/wx/page/entryadd', methods=['GET'])
@login_required
def entry_page_add():
    return render_template('wx/entryadd.html', **locals())


@app.route('/wx/data/entryadd', methods=['POST'])
@login_required
def entry_data_add():
    data = request.get_json()
    userEntry = UserEntry(data['userid'], data['username'], data['appid'], data['appsecret'], data['apptype'],
                          data['sortednum'])
    userEntry.save()
    return jsonify({'status': 'success'})


@app.route('/wx/data/tokenreview', methods=['GET'])
@login_required
def token_data_create():
    appId = request.args.get('appid')
    queryTokes = AccessToken.query.filter_by(appid = appId).all()
    if queryTokes:
        for token in queryTokes:
            token.update()
    else:
        userEntry = UserEntry.query.filter_by(appid=appId).first()
        AccessToken.CreateToken(userEntry.appid, userEntry.appsecret)
    return jsonify({'status': 'success'})


#################################################公众号管理 end#########################################################

#################################################公众号页面 start#######################################################
@app.route('/wx/page/test1', methods=['GET'])
def pageTest1():
    return render_template('wx/page/test1.html', **locals())


@app.route('/wx/page/test2', methods=['GET'])
def pageTest2():
    url = request.url
    # appId = request.args.get('appid')
    appId = 'wx91e620b9e343d193'
    jsapiToken = AccessToken.query.filter(and_(AccessToken.appid == appId, AccessToken.type == 1)).first()
    sign = Sign(jsapiToken.token if jsapiToken else '', url)
    # accessToken = AccessToken.query.get(appId)
    return render_template('wx/page/test3.html', **{'sign': sign.sign()})

#################################################公众号页面 end#########################################################
