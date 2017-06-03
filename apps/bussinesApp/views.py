#-*- coding:utf-8 -*-
#!/usr/bin/env python
from flask import render_template
from apps.bussinesApp import bussines


@bussines.route('/')
def Index():
    return render_template('bussines.html', **locals())