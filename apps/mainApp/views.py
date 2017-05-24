#-*- coding:utf-8 -*-
#!/usr/bin/env python
import json
import urllib

__author__ = 'hukekuan'
from flask import g,request,make_response,flash,render_template,Response
from apps import app

@app.route('/')
def index():
    return render_template('index.html', **locals())


