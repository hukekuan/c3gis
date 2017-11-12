#-*- coding:utf-8 -*-
#!/usr/bin/env python
from flask_restful.inputs import date,url
from flask_restful import Resource, fields, marshal_with,reqparse
from apps.apiApp import fields as jf_fields


nested_tag_fields = {
    'id': fields.String(),
    'name': fields.String()}
post_fields = {
    'author': fields.String("hukeuna"),
    'title': fields.String(),
    'text': jf_fields.HTMLField(),
    'tags': fields.List(fields.Nested(nested_tag_fields)),
    'publish_date': fields.DateTime(dt_format='iso8601')}

class HelloWorld(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, location='args')
        args = parser.parse_args()
        print(args['name'])

        if args['name']:
            return {'hello': args['name']}
        else:
            return {'hello': 'params'}

