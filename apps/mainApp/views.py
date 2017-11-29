#-*- coding:utf-8 -*-
#!/usr/bin/env python
import json
from flask import g, request, make_response, flash, render_template, redirect, url_for, current_app, jsonify
from flask_login import login_user, login_required, current_user, logout_user
from apps.mainApp.CustomerException import InvalidUsage
from apps.mainApp.forms import LoginForm
from apps.mainApp.models import User, UserEncoder
from apps import app

@app.before_request
def before_request():
    g.user = current_user

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(InvalidUsage)
def page_not_found(error):
    print(error.message)
    return render_template('500.html'), 500

@app.route('/')
@login_required
def index():
    username = g.user.username
    return render_template('index.html', **locals())


########################################Form Login###################################################

@app.route('/login',methods=['GET','POST'])
def login():
    # current_app.logger.error('**********Login Login**********')
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


########################################System Manage###################################################
# 用户管理界面
@app.route('/sys/usermanage')
@login_required
def usermanage():
    return render_template('sys/usermanage.html', **locals())

@app.route('/sys/page/useradd',methods=['GET'])
@login_required
def user_page_add():
    if request.method == 'POST':
        print(request)
    return render_template('sys/useradd.html', **locals())

@app.route('/sys/data/useradd',methods=['POST'])
@login_required
def user_data_add():
    data = request.get_json()
    print(data)
    user = User(data['username'],data['email'],data['password'])
    user.save()
    return jsonify({'status':'success'})


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



@app.route('/test',methods=['GET'])
@login_required
def Test():
    return jsonify({'data': 'Hello, %s!' % g.user.username})

