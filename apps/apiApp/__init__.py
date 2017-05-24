#-*- coding:utf-8 -*-
#!/usr/bin/env python

from flask import Blueprint
from flask_restful import Api
from apps.apiApp.views import HelloWorld

api_bp = Blueprint('api',__name__)

api = Api(api_bp)
api.add_resource(HelloWorld,'/test/<name>')

