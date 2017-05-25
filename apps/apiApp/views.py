#-*- coding:utf-8 -*-
#!/usr/bin/env python

from flask_restful import Resource, reqparse



class HelloWorld(Resource):
    def get(self,name):
        return {'hello': 'world '+ name}

    def post(self,name):
        parser = reqparse.RequestParser()
        parser.add_argument('task', type=str)
        args = parser.parse_args()
        print(args)
        return {'status': 'success'}
