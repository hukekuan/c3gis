#-*- coding:utf-8 -*-
#!/usr/bin/env python

# APPID = 'wx71713e35af6fc0a8'
# APPSECRET = '92a6fae7306f9fdd03235972d0e6ef0c'

# 测试账号
# APPID = 'wx91e620b9e343d193'
# APPSECRET = 'e761256f03304edf6ae2b90db1e6a7c7'

# redis缓存数据库配置
REDIS = {
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_HOST': '127.0.0.1',
    'CACHE_REDIS_PORT': 6379,
    'CACHE_REDIS_DB': '',
    'CACHE_REDIS_PASSWORD': ''
}


#Schduler config
JOBS = [
    {
        'id': 'test_job',
        'func': 'apps.wxApp.job:accesTokenReview_job',
        'args': None,
        'trigger': 'interval',
        'seconds': 5*60
    }
]