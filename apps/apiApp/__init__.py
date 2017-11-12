#-*- coding:utf-8 -*-
#!/usr/bin/env python
from flask import Blueprint
from apps import api
from apps.apiApp.views import HelloWorld

apiApp = Blueprint('apiApp',__name__,template_folder='templates',static_folder='static')

api.add_resource(HelloWorld, '/api/test')