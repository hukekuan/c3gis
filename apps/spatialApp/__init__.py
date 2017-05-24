#-*- coding:utf-8 -*-
#!/usr/bin/env python
from flask import Blueprint

spatial = Blueprint('spatial',__name__,template_folder='templates',static_folder='static')

from apps.spatialApp import views
