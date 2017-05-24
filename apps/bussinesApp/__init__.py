#-*- coding:utf-8 -*-
#!/usr/bin/env python
from flask import Blueprint

bussines = Blueprint('bussines',__name__,template_folder='templates',static_folder='static')

from apps.bussinesApp import views