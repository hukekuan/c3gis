#-*- coding:utf-8 -*-
#!/usr/bin/env python

class InvalidUsage(Exception):
    status_code = 400
    def __init__(self, message, status_code=400):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code