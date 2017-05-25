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

print(config['development'].SQLALCHEMY_DATABASE_URI)
app.config.from_object(config['development'])
app.config.from_pyfile('custom_config.py')
db = SQLAlchemy(app)
cache = SimpleCache()

from apps.bussinesApp import bussines
from apps.spatialApp import spatial
from apps.apiApp import api_bp
from apps.mainApp import main

app.register_blueprint(bussines,url_prefix='/bussines')
app.register_blueprint(spatial,url_prefix='/spatial')
app.register_blueprint(api_bp,url_prefix='/api')
app.register_blueprint(main)





