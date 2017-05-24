#-*- coding:utf-8 -*-
#!/usr/bin/env python

class Config(object):
    DEBUG = False
    TESTING = False

class ProductionConfig(Config):
    # SQLALCHEMY_DATABASE_URI = 'mysql://w3kx210mn4:y00xy3hxk14i11lwz1w4x52044ww52z0mzl01mil@w.rdc.sae.sina.com.cn:3307/app_c3gis'
    # SQLALCHEMY_DATABASE_URI = 'oracle://hb:hb@172.16.0.251:1521/hbzb'
    # SQLALCHEMY_BINDS = {
    #     'gisdb' :'postgresql://postgres:postgres@localhost/gisdb'
    # }
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    # SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@localhost/testdb'
    # # SQLALCHEMY_DATABASE_URI = 'oracle://spatial:spatial@172.16.6.13:1521/ORCL'
    # SQLALCHEMY_BINDS = {
    #     'online':'oracle://hb:hb@172.16.0.251:1521/hbzb',
    #     'gisdb': 'postgresql://postgres:postgres@localhost/gisdb'
    # }
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_ECHO = True
    # DEBUG = True

class TestingConfig(Config):
    # SQLALCHEMY_DATABASE_URI = 'oracle://hb:hb@172.16.0.251:1521/hbzb'
    # SQLALCHEMY_BINDS = {
    #     'gisdb': 'postgresql://postgres:postgres@localhost/gisdb'
    # }
    # TESTING = True
    pass

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}