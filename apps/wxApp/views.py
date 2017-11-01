#-*- coding:utf-8 -*-
#!/usr/bin/env python
import json
import sys
import time
import urllib
from flask import render_template
from apps.wxApp.utils import parse_xml

reload(sys)
sys.setdefaultencoding('utf-8')
from flask import request

from apps.wxApp import wx

# @wx.route('/token',methods=['GET','POST'])
# def Token():
#     result = request.args['echostr']
#     return result


@wx.route('/token',methods=['GET','POST'])
def Token():
    if True:
        receiveMsg = parse_xml(request.data)
        XmlForm = """
                <xml>
                <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
                <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
                <CreateTime>{CreateTime}</CreateTime>
                <MsgType><![CDATA[news]]></MsgType>
                <ArticleCount>2</ArticleCount>
                <Articles>
                <item>
                <Title><![CDATA[中乌发动机合作生变？乌克兰地方法院冻结中资股份]]></Title>
                <PicUrl><![CDATA[http://c3gis-c3gis.stor.sinaapp.com/images/a.jpeg]]></PicUrl>
                <Url><![CDATA[http://c3gis.applinzi.com]]></Url>
                </item>
                <item>
                <Title><![CDATA[中国新型无人武直惊艳亮相，优势独特全世界仅3国能造]]></Title>
                <PicUrl><![CDATA[http://c3gis-c3gis.stor.sinaapp.com/images/a.jpeg]]></PicUrl>
                <Url><![CDATA[http://c3gis.applinzi.com]]></Url>
                </item>
                </Articles>
                </xml>
            """
        info = dict()
        info['ToUserName'] = receiveMsg.FromUserName
        info['FromUserName'] = receiveMsg.ToUserName
        info['CreateTime'] = int(time.time())

        return XmlForm.format(**info)