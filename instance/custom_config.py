#-*- coding:utf-8 -*-
#!/usr/bin/env python

# APPID = 'wx71713e35af6fc0a8'
# APPSECRET = '92a6fae7306f9fdd03235972d0e6ef0c'

# 测试账号
# APPID = 'wx91e620b9e343d193'
# APPSECRET = 'e761256f03304edf6ae2b90db1e6a7c7'



#Schduler config
JOBS = [
    {
        'id': 'test_job',
        'func': 'apps.bussinesApp.job:quote_send_sh_job',
        'args': None,
        'trigger': 'interval',
        'seconds': 5
    }
]