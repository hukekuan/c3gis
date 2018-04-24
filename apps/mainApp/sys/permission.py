#-*- coding:utf-8 -*-
#!/usr/bin/env python
from flask_principal import Permission, RoleNeed

admin_permission = Permission(RoleNeed('admin'))
poster_permission = Permission(RoleNeed('poster'))
default_permission = Permission(RoleNeed('default'))

def admin_authority(func):
    def decorated_view(*args,**kwargs):
        if admin_permission.can():
            return func(*args,**kwargs)
        else:
            return "非Admin用户"

    return decorated_view