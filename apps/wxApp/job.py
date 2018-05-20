#-*- coding:utf-8 -*-
#!/usr/bin/env python
from apps import app
from apps.wxApp.models.wxentry import AccessToken


def accesTokenReview_job():
    with app.app_context():
        tokenList = AccessToken.query.all()
        if tokenList:
            for token in tokenList:
                token.update()