#-*- coding:utf-8 -*-
#!/usr/bin/env python

# APPID = 'wx71713e35af6fc0a8'
# APPSECRET = '9a596c610bf71cbb2ab9fc71d3219ed4'

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