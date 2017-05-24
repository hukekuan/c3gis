#-*- coding:utf-8 -*-
#!/usr/bin/env python

from flask_restful import Resource

class HelloWorld(Resource):
    def get(self,name):
        return {'hello': 'world '+ name}
