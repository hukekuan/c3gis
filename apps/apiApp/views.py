#-*- coding:utf-8 -*-
#!/usr/bin/env python
from flask import jsonify
from flask_restful import Resource, reqparse

from apps.apiApp.models import Chart


class HelloWorld(Resource):
    def get(self,name):
        return {'hello': 'world '+ name}

    def post(self,name):
        parser = reqparse.RequestParser()
        parser.add_argument('task', type=str)
        args = parser.parse_args()
        print(args)
        return {'status': 'success'}

class CreateEcharts(Resource):
    def get(self):
        pass
    def post(self):
        return None

class GetEcharts(Resource):
    def get(self,name):
        selectedChart = Chart.query.filter_by(name='11').first()
        return jsonify(selectedChart.chart)