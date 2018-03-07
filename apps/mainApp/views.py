#-*- coding:utf-8 -*-
#!/usr/bin/env python

import json
from flask import g, request, make_response, flash, render_template, redirect, url_for, current_app, jsonify
from flask_login import login_user, login_required, current_user, logout_user
from flask_principal import identity_changed, Identity, AnonymousIdentity

from apps.mainApp.CustomerException import InvalidUsage
from apps.mainApp.forms import LoginForm
from apps.mainApp.models import User, UserEncoder, TableResult, TableResultEncoder, Role, RoleEncoder
from apps import app, db


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
            identity_changed.send(
                current_app._get_current_object(),
                identity=Identity(user.userid))

            return redirect(request.args.get('next') or url_for('index'))
        flash('Invalid username or password.')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    identity_changed.send(
        current_app._get_current_object(),
        identity=AnonymousIdentity())
    return redirect(url_for('login'))


########################################用户管理###################################################
# 用户管理界面
@app.route('/sys/usermanage')
@login_required
def usermanage():
    return render_template('sys/usermanage.html', **locals())

@app.route('/sys/page/useradd',methods=['GET'])
@login_required
def user_page_add():
    return render_template('sys/useradd.html', **locals())

@app.route('/sys/data/useradd',methods=['POST'])
@login_required
def user_data_add():
    data = request.get_json()
    user = User(data['username'],data['email'],data['password'])
    user.save()
    return jsonify({'status':'success'})

@app.route('/sys/data/userdelete',methods=['POST'])
@login_required
def user_data_delete():
    userIds = request.get_json()
    if userIds:
        for userId in userIds:
            user = User.query.filter_by(userid = userId).first()
            db.session.delete(user)
        db.session.commit()
    return jsonify({'status': 'success'})


#用户列表
@app.route('/sys/userlist',methods=['GET'])
@login_required
def userlist():
    page = int(request.args.get('page'))
    limit = int(request.args.get('limit'))
    userPagination = User.query.order_by(User.sortednum).paginate(page,limit)
    userlist = userPagination.items
    tableResult = TableResult(
        userPagination.pages * limit,
        json.loads(json.dumps(userlist, cls=UserEncoder)),
        0,""
    )
    return json.dumps(tableResult, cls=TableResultEncoder)

@app.route('/sys/page/rolebind',methods=['GET'])
@login_required
def user_page_rolebind():
    userid = request.args.get('userid')
    return render_template('sys/rolebind.html', **locals())

@app.route('/sys/data/rolebind',methods=['POST'])
@login_required
def user_rolebind():
    result = {'status': 'error'}
    data = request.get_json()
    queryUser = User.query.get(data['userId'])
    if queryUser:
        if not queryUser:
            queryUser.roles = []
        else:
            queryUser.roles = Role.query.filter(Role.roleid.in_(data['roleIds'])).all()
        db.session.commit()
        result['status'] = 'success'
    return jsonify(result)
########################################角色管理###################################################
@app.route('/sys/rolemanage')
@login_required
def rolemanage():
    return render_template('sys/rolemanage.html', **locals())


#角色列表
@app.route('/sys/rolelist',methods=['GET'])
@login_required
def rolelist():
    page = int(request.args.get('page'))
    limit = int(request.args.get('limit'))
    rolePagination = Role.query.order_by(Role.sortednum).paginate(page,limit)
    rolelist = rolePagination.items
    tableResult = TableResult(
        rolePagination.pages * limit,
        json.loads(json.dumps(rolelist, cls=RoleEncoder)),
        0,""
    )
    return json.dumps(tableResult, cls=TableResultEncoder)

@app.route('/sys/rolebyuser',methods=['GET'])
@login_required
def roleListByUserId():
    userId = request.args.get('userid')
    queryUser = User.query.get(userId)
    roleIds = [role.roleid for role in queryUser.roles]
    roleLsit = json.loads(json.dumps(Role.query.all(), cls=RoleEncoder))
    if roleLsit:
        for role in roleLsit:
            if role['roleid'] in roleIds:
                role['LAY_CHECKED'] = True
    tableResult = TableResult(
        len(roleLsit),
        roleLsit,
        0, ""
    )
    return json.dumps(tableResult, cls=TableResultEncoder)

# 角色添加页面
@app.route('/sys/page/roleadd',methods=['GET'])
@login_required
def role_page_add():
    return render_template('sys/roleadd.html', **locals())

# 角色添加数据接口
@app.route('/sys/data/roleadd',methods=['POST'])
@login_required
def role_data_add():
    data = request.get_json()
    role = Role(data['rolename'],data['description'] if 'description' in data.keys() else '', data['sortednum'])
    role.save()
    return jsonify({'status':'success'})