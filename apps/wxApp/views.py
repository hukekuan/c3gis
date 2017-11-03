#-*- coding:utf-8 -*-
#!/usr/bin/env python

import sys
import time

from apps.wxApp.models.wxmessage import ArticleItem, ArticleMsg
from apps.wxApp.utils import parse_xml

reload(sys)
sys.setdefaultencoding('utf-8')
from flask import request

from apps.wxApp import wx

@wx.route('/token',methods=['GET','POST'])
def Token():
    if request.method == 'GET' and 'echostr' in request.args.keys():
        result = request.args['echostr']
        return result
    elif request.method == 'POST':
        receiveMsg = parse_xml(request.data)

        articleItem1=ArticleItem(
            '中乌发动机合作生变？乌克兰地方法院冻结中资股份',
            'http://c3gis-c3gis.stor.sinaapp.com/images/a.jpeg',
            'http://c3gis.applinzi.com')
        articleItem2 = ArticleItem(
            '中国新型无人武直惊艳亮相，优势独特全世界仅3国能造',
            'http://c3gis-c3gis.stor.sinaapp.com/images/a.jpeg',
            'http://c3gis.applinzi.com')
        articleMsg = ArticleMsg(receiveMsg.FromUserName,receiveMsg.ToUserName,[articleItem1,articleItem2])

        return articleMsg.xmlFormat()