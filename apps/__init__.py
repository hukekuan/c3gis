#-*- coding:utf-8 -*-
#!/usr/bin/env python
import os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
import logging
from flask import Flask
from flask_apscheduler import APScheduler
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_login import LoginManager, current_user
from flask_principal import Principal, RoleNeed, UserNeed, identity_loaded
from werkzeug.contrib.cache import SimpleCache

app = Flask(__name__,template_folder='templates',static_folder='static',instance_relative_config=True)

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

app.config.from_object(config['development'])
app.config.from_pyfile('custom_config.py')

errorHandler = logging.FileHandler('error.log', encoding='UTF-8')
errorHandler.setLevel(logging.ERROR)
error_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s \r\n%(message)s\r\n')


errorHandler.setFormatter(error_format)
app.logger.addHandler(errorHandler)

db = SQLAlchemy(app)
cache = SimpleCache()

loginManager = LoginManager()
loginManager.init_app(app)
loginManager.session_protection = "strong"
loginManager.login_view = "login"



principals = Principal()
principals.init_app(app)
@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
        '''
            Change the role via add the Need object into Role.
            Need the access the app object.
        '''
        identity.user = current_user
        # Add the UserNeed to the identity user object
        if hasattr(current_user,'userid'):
                identity.provides.add(UserNeed(current_user.userid))
        # Add each role to the identity user object
        if hasattr(current_user,'roles'):
                for role in current_user.roles:
                        identity.provides.add(RoleNeed(role.rolename))



from apps.bussinesApp import bussines
from apps.wxApp import wx
from apps.mainApp import main

app.register_blueprint(bussines, url_prefix='/bussines')
app.register_blueprint(wx, url_prefix='/wx')
app.register_blueprint(main)



scheduler=APScheduler()
scheduler.init_app(app)
scheduler.start()





