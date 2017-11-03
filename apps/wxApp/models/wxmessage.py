#-*- coding:utf-8 -*-
#!/usr/bin/env python
import string
import time

class ArticleItem(object):
    def __init__(self,title,picUrl,url):
        self.title=title
        self.picUrl=picUrl
        self.url=url
    def xmlFormat(self):
        resultStr = '<item><Title><![CDATA[{0}]]></Title><PicUrl><![CDATA[{1}]]></PicUrl><Url><![CDATA[{2}]]></Url></item>'
        return resultStr.format(*[self.title,self.picUrl,self.url])

class ReceiveMsg(object):
    def __init__(self,fromUserName,toUserName):
        self.fromUserName=fromUserName
        self.toUserName=toUserName
    def xmlFormat(self):
        resultStr='<xml><ToUserName><![CDATA[{0}]]></ToUserName><FromUserName><![CDATA[{1}]]></FromUserName><CreateTime>{2}</CreateTime>'
        return resultStr.format(*[self.fromUserName,self.toUserName,int(time.time())])

class ArticleMsg(ReceiveMsg):
    def __init__(self,fromUserName,toUserName,articleItems):
        super(ArticleMsg,self).__init__(fromUserName,toUserName)
        self.articleItems = articleItems

    def xmlFormat(self):
        resultStr = '<MsgType><![CDATA[news]]></MsgType><ArticleCount>{0}</ArticleCount><Articles>'.format(*[len(self.articleItems)])
        itemStr = [item.xmlFormat() for item in self.articleItems]

        return string.join([super(ArticleMsg,self).xmlFormat(),resultStr,string.join(itemStr,''),'</Articles></xml>'],'')
