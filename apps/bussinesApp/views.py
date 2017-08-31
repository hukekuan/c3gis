#-*- coding:utf-8 -*-
#!/usr/bin/env python
from flask import render_template
from apps.bussinesApp import bussines


@bussines.route('/')
def Login():
    return render_template('login.html', **locals())

@bussines.route('/main')
def Main():
    return render_template('bussines.html', **locals())