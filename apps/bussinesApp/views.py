#-*- coding:utf-8 -*-
#!/usr/bin/env python

from flask import render_template, app
from apps.bussinesApp import bussines
from flask import request
from apps.bussinesApp.utils import Sign
# from apps.mainApp.models import Token
# from apps.mainApp.models import getTicket


@bussines.route('/air/location')
def airLocation():
    # jsapi_ticket=getTicket().tokenvalue
    # url = request.url
    # sign = Sign(jsapi_ticket, url).sign()
    # return render_template('wxindex.html',sign=sign)
    pass


@bussines.route('/air/region')
def airRegion():
    # jsapi_ticket = getTicket().tokenvalue
    # url = request.url
    # sign = Sign(jsapi_ticket, url).sign()
    # return render_template('ui.html',sign=sign)
    pass


@bussines.route('/sufacewater')
def Sufacewater():
    return render_template('index.html', **locals())


@bussines.route('/pollutionsource/exhaustgas')
def Exhaustgas():
    return render_template('index.html', **locals())


@bussines.route('/pollutionsource/wastewater')
def Wastewater():
    return render_template('index.html', **locals())


@bussines.route('/pollutionsource/stp')
def Stp():
    return render_template('index.html', **locals())


@bussines.route('/ui')
def UI():
    return render_template('ui.html', **locals())


#=========================================Vue.js=================================================
@bussines.route('/vue/demo')
def VueDemo():
    return render_template('vue/demo.html')
    # return bussines.send_static_file('demo.html')

@bussines.route('/vue/mintui/first')
def First():
    return render_template('vue/mintui/first.html')

