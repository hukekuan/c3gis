#-*- coding:utf-8 -*-
#!/usr/bin/env python
import os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_login import LoginManager
from werkzeug.contrib.cache import SimpleCache

app = Flask(__name__,template_folder='templates',static_folder='static',instance_relative_config=True)

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

app.config.from_object(config['development'])
app.config.from_pyfile('custom_config.py')
db = SQLAlchemy(app)
cache = SimpleCache()

loginManager = LoginManager()
loginManager.init_app(app)
loginManager.session_protection = "strong"
loginManager.login_view = "login"

from apps.bussinesApp import bussines
from apps.spatialApp import spatial
from apps.mainApp import main

app.register_blueprint(bussines,url_prefix='/bussines')
app.register_blueprint(spatial,url_prefix='/spatial')
app.register_blueprint(main)





