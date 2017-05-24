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


@app.route('/MP_verify_d27KRyv47e80atfj.txt')
def Test():
    return make_response('d27KRyv47e80atfj')

@app.route('/token',methods=['GET','POST'])
def Token():
    mesg = "<xml><ToUserName><![CDATA[o-b3c1YkGj1n8IlVqvzBPEJz6F2I]]></ToUserName><FromUserName><![CDATA[gh_67d31e68bad2]]></FromUserName><CreateTime>12345678</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA['是你吗']]></Content></xml>"

    # for tmp in request.args:
    #     mesg = tmp + "=" + str(request.args[tmp]) + ";"
    http_str = 'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=lOcUku6fS0rZ0YDmVWapLtoaTORb-OKK6nYuy1giSoV8jjQ3ITnVs9yL0bE6PKOEPohPdJR1Yz7_NEPFfHlZzVnjd0qLisYxGt9p3RQ3jMwHBQiAFALFU'
    params1 = {
        "touser": "o-b3c1YkGj1n8IlVqvzBPEJz6F2I",
        "msgtype": "text",
        "text": {
            "content": u'胡克宽'
        }
    }
    params = json.dumps(params1)
    response = urllib.urlopen(http_str, (params))
    #
    # return 'success'
    return ''



@app.route('/oauth')
def Oauth():
    return render_template('oauth.html', code=request.args['code'])
@app.route('/dbinit',methods=['GET'])
def dbInit():
    return render_template('index.html', **locals())
