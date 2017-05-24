#-*- coding:utf-8 -*-
#!/usr/bin/env python
from flask import Blueprint

spatial = Blueprint('spatial',__name__)

from apps.spatialApp import views
