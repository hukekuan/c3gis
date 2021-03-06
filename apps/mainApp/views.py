#-*- coding:utf-8 -*-
#!/usr/bin/env python

import json

import time
from flask import g, request, make_response, flash, render_template, redirect, url_for, current_app, jsonify
from flask_login import login_user, login_required, current_user, logout_user
from flask_principal import identity_changed, Identity, AnonymousIdentity

from apps.mainApp.CustomerException import InvalidUsage
from apps.mainApp.forms import LoginForm
from apps.mainApp.models import User, UserEncoder, TableResult, TableResultEncoder, Role, RoleEncoder, Menu, \
    MenuEncoder, Org
from apps import app, db
from apps.wxApp.utils import parse_xml


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
    if g.user is None or not g.user.is_authenticated:
        return redirect(url_for('login'))
    username = g.user.username
    return render_template('index.html', **locals())

@app.route('/token',methods=['GET','POST'])
def WXToken():
    receiveMsg = parse_xml(request.data)
    XmlForm = """
                <xml>
                <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
                <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
                <CreateTime>{CreateTime}</CreateTime>
                <MsgType><![CDATA[text]]></MsgType>
                <Content>hukekuan</Content>
                </xml>
            """
    info = dict()
    info['ToUserName'] = receiveMsg.FromUserName
    info['FromUserName'] = receiveMsg.ToUserName
    info['CreateTime'] = int(time.time())

    return XmlForm.format(**info)
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


########################################用户管理 start###################################################
# 用户管理界面
@app.route('/sys/usermanage')
@login_required
def usermanage():
    return render_template('sys/usermanage.html', **locals())

@app.route('/sys/page/useradd',methods=['GET'])
@login_required
def user_page_add():
    orgId = request.args.get('orgid')
    return render_template('sys/useradd.html', **locals())

@app.route('/sys/data/useradd',methods=['POST'])
@login_required
def user_data_add():
    data = request.get_json()
    org = Org.query.get(data['orgid'])
    user = User(data['username'],data['email'],data['password'],int(data['sortednum']))
    if org.users:

        org.users.append(user)
    else:
        org.users = [user]
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
    orgId = request.args.get('orgid')
    if not orgId or orgId == '0':
        userPagination = User.query.order_by(User.sortednum).paginate(page,limit)
        totalCount = userPagination.pages * limit
        userlist = userPagination.items
    else:
        userlistByOrg = Org.query.get(orgId).users
        userlistByOrg.sort(key= lambda user:user.sortednum)
        totalCount = len(userlistByOrg)
        if not userlistByOrg:
            userlist = userlistByOrg[limit*(page-1):totalCount]
        else:
            userlist = userlistByOrg
    tableResult = TableResult(
        totalCount,
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
########################################用户管理 end###############################################


########################################组织机构 start#############################################

@app.route('/sys/data/orglist',methods=['GET'])
@login_required
def orglist():
    orgList = Org.query.order_by(Org.sortednum).all()
    if orgList:
        result = [{'name':org.orgname,'id':org.orgid} for org in orgList]
    else:
        result = list()
    return jsonify(result)

@app.route('/sys/page/orgadd',methods=['GET'])
@login_required
def org_page_add():
    parentid = request.args.get('parentid')
    return render_template('sys/orgadd.html', **locals())

@app.route('/sys/data/orgadd',methods=['POST'])
@login_required
def org_data_add():
    data = request.get_json()
    print(data)
    org = Org(data['parentid']
              , data['orgname']
              , data['sortednum']
              , data['regioncode']
              , data['address']
              , data['telephone']
              , data['email']
              , data['administr']
              , data['description']
    )
    org.save()
    return jsonify({'status':'success'})

########################################组织机构 end###############################################


########################################角色管理 start#############################################
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

# 角色绑定菜单页面
@app.route('/sys/page/correlatemenu',methods=['GET'])
@login_required
def role_page_correlatemenu():
    roleid = request.args.get('roleid')
    return render_template('sys/correlatemenu.html', **locals())

@app.route('/sys/data/rolemenus',methods=['GET'])
@login_required
def role_data_rolemenus():
    roleid = request.args.get('roleid')
    correlatedMenus = Role.query.get(roleid).menus
    correlatedMenuIds = [menu.menuid for menu in correlatedMenus]

    menuList = Menu.query.all()
    result = getMenusByParentId(menuList,'0',correlatedMenuIds)
    if result:
        for menu in result:
            menu['data'] = getMenusByParentId(menuList,menu['value'],correlatedMenuIds)
            if menu['data']:
                for childMenu in menu['data']:
                    childMenu['data'] = getMenusByParentId(menuList,childMenu['value'],correlatedMenuIds)
    return jsonify(result)

@app.route('/sys/data/correlatemenu',methods=['POST'])
@login_required
def role_data_correlatemenu():
    data = request.get_json()
    selectRole = Role.query.get(data['roleid'])
    if data['menuids']:
        selectRole.menus = Menu.query.filter(Menu.menuid.in_(data['menuids'])).all()
    else:
        selectRole.menus =[]
    db.session.commit()
    return jsonify({'status': 'success'})

def getMenusByParentId(menuList,parenId,correlatedMenuIds):
    if menuList and parenId:
        selectedMenus = filter(lambda menu: menu.parentid == parenId, menuList)
        result = [checkMenuCorrelate(correlatedMenuIds,resultMenu) for resultMenu in selectedMenus]
    else:
        result = list()
    return result

def checkMenuCorrelate(correlatedMenuIds,selectMenu):
    result = {'title': selectMenu.menuname, 'value': selectMenu.menuid,'data': []}
    if correlatedMenuIds and selectMenu.menuid in correlatedMenuIds:
        result['checked'] = True
    return result

########################################角色管理 end#############################################



########################################菜单管理 start############################################
# 菜单管理页面
@app.route('/sys/menumanage')
@login_required
def menumanage():

    return render_template('sys/menumanage.html', **locals())

# 菜单列表
@app.route('/sys/pagemenus', methods=['GET'])
@login_required
def menulistBypage():
    page = int(request.args.get('page'))
    limit = int(request.args.get('limit'))
    parentid = str(request.args.get('parentid')) if 'parentid' in request.args.keys() else '0'
    menuPagination = Menu.query.filter_by(parentid = parentid).order_by(Menu.sortednum).paginate(page, limit)
    menulist = menuPagination.items
    tableResult = TableResult(
        menuPagination.pages * limit,
        json.loads(json.dumps(menulist, cls=MenuEncoder)),
        0, ""
    )
    return json.dumps(tableResult, cls=TableResultEncoder)


@app.route('/sys/menulist', methods=['GET'])
@login_required
def menulist():
    result = list()
    firstMenus = Menu.query.filter(
                Menu.parentid=='0',
                Menu.isfront==False).order_by(Menu.sortednum).all()
    if firstMenus:
        for firstMenu in firstMenus:
            first = {
                'text': firstMenu.menuname,
                'icon': firstMenu.icon
            }
            secondMenus = Menu.query.filter(
                Menu.parentid==firstMenu.menuid,
                Menu.isfront==False).order_by(Menu.sortednum).all()
            if secondMenus:
                first['subset'] = list()
                for secondMenu in secondMenus:
                    first['subset'].append({
                        'text': secondMenu.menuname,
                        'icon': secondMenu.icon,
                        'href':secondMenu.href
                    })
            result.append(first)
    return jsonify(result)


# 菜单添加页面
@app.route('/sys/page/menuadd', methods=['GET'])
@login_required
def menu_page_add():
    parentid = request.args.get('parentid')
    return render_template('sys/menuadd.html',  **locals())

# 菜单添加数据接口
@app.route('/sys/data/menuadd', methods=['POST'])
@login_required
def menu_data_add():
    data = request.get_json()
    menu = Menu(
        data['parentid'] if data['parentid'] else '0',
        data['menuname'],
        data['href'],
        data['target'],
        data['icon'],
        data['menutype'],
        data['isshow'],
        data['isfront'],
        data['sortednum']
    )
    # role = Role(data['rolename'], data['description'] if 'description' in data.keys() else '', data['sortednum'])
    menu.save()
    return jsonify({'status': 'success'})

@app.route('/sys/data/menuparent', methods=['GET'])
@login_required
def menu_getParentId():
    menutid = str(request.args.get('menutid'))
    queryMenu = Menu.query.get(menutid)
    return jsonify({'parentid':queryMenu.parentid if queryMenu else ""})

@app.route('/sys/data/menulist', methods=['GET'])
@login_required
def menuListByRole():
    currentRole = g.user.roles
    if currentRole:
        resultMenus = filter(lambda menu: menu.isshow, currentRole[0].menus)
    else:
        resultMenus = []

    return json.dumps(resultMenus, cls=MenuEncoder)

@app.route('/sys/data/menudelete', methods=['POST'])
@login_required
def menuDeleteById():
    menuIds = request.get_json()
    selectedMenus=list()
    if menuIds:
        for menuId in menuIds:
            selectedMenu = Menu.query.get(menuId)
            selectedMenu.delete()
    return jsonify({'status': 'success'})
########################################菜单管理 end##############################################