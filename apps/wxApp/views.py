#-*- coding:utf-8 -*-
#!/usr/bin/env python
import json
import sys
import time
import urllib

from flask import render_template

reload(sys)
sys.setdefaultencoding('utf-8')
from flask import request

from apps.wxApp import wx

@wx.route('/',methods=['GET','POST'])
def Token():
    result = request.args['echostr']
    return result

@wx.route('/test')
def Test():
    return render_template('wx/wxindex.html', **locals())