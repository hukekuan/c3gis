#-*- coding:utf-8 -*-
#!/usr/bin/env python
from flask import Blueprint

wx = Blueprint('wx',__name__,template_folder='templates',static_folder='static')

from apps.wxApp import views
