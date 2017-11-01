#-*- coding:utf-8 -*-
#!/usr/bin/env python
import json
import os

from flask import g, request, make_response, flash, render_template, redirect, url_for, jsonify
from flask_login import login_user, login_required, current_user, logout_user
from apps.mainApp.forms import LoginForm
from apps.mainApp.models import User, UserEncoder
from apps import app

@app.before_request
def before_request():
    g.user = current_user

@app.route('/<path>')
def today(path):
    base_dir = os.path.dirname(__file__)
    resp = make_response(open(os.path.join(base_dir, path)).read())
    # resp.headers["Content-type"]="application/json;charset=UTF-8"
    resp.headers["Content-type"] = "charset=UTF-8"
    return resp



@app.route('/')
@login_required
def index():
    # resp = make_response('Hello World!')
    # flash('You were successfully logged in')
    username = g.user.username
    return render_template('index.html', **locals())

@app.route('/login',methods=['GET','POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    # if request.method == 'POST' and form.validate_on_submit():
    if request.method == 'POST':
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, True)
            g.user = user
            return redirect(request.args.get('next') or url_for('index'))
        flash('Invalid username or password.')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# 用户管理界面
@app.route('/sys/usermanage')
@login_required
def usermanage():
    return render_template('sys/usermanage.html', **locals())
@app.route('/sys/page/useradd')
@login_required
def user_page_add():
    return render_template('sys/useradd.html', **locals())


#用户列表
@app.route('/sys/userlist',methods=['GET'])
@login_required
def userlist():
    userlist = User.query.all()
    return make_response(json.dumps(userlist, cls=UserEncoder))


@app.route('/sys/rolemanage')
@login_required
def rolemanage():
    return render_template('sys/rolemanage.html', **locals())

