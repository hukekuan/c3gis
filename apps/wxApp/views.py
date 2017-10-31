#-*- coding:utf-8 -*-
#!/usr/bin/env python
__author__ = 'hukekuan'

from flask import render_template, app
from apps.wxApp import wx

@wx.route('/token')
def index():
    return render_template('wx/wxindex.html')