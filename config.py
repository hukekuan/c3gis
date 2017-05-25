#-*- coding:utf-8 -*-
#!/usr/bin/env python

class Config(object):
    DEBUG = False
    TESTING = False

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost/gisdb'
    # SQLALCHEMY_DATABASE_URI = 'oracle://hb:hb@172.16.0.251:1521/hbzb'
    # SQLALCHEMY_BINDS = {
    #     'gisdb' :'postgresql://postgres:postgres@localhost/gisdb'
    # }
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    # SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@localhost/testdb'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost/gisdb'
    SQLALCHEMY_BINDS = {
        # 'online':'oracle://hb:hb@172.16.0.251:1521/hbzb',
        # 'gisdb': 'postgresql://postgres:postgres@localhost/gisdb'
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    DEBUG = True

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost/gisdb'
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