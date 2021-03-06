#-*- coding:utf-8 -*-
#!/usr/bin/env python
import string
import time

##################################################文本消息#######################################################
class TextMsg(object):
    def __init__(self, fromUserName, toUserName,text):
        self.fromUserName = fromUserName
        self.toUserName = toUserName
        self.text = text

    def xmlFormat(self):
        resultStr = '''
        <xml>
            <ToUserName>< ![CDATA[{toUser}] ]></ToUserName>
            <FromUserName>< ![CDATA[{fromUser}] ]></FromUserName>
            <CreateTime>{createTime}</CreateTime>
            <MsgType>< ![CDATA[text] ]></MsgType>
            <Content>< ![CDATA[{text}] ]></Content>
        </xml>
        '''

##################################################图片消息#######################################################
class imageMsg(object):
    def __init__(self, fromUserName, toUserName,text):
        self.fromUserName = fromUserName
        self.toUserName = toUserName
        self.text = text

    def xmlFormat(self):
        resultStr = '''
        <xml>
        <ToUserName>< ![CDATA[{toUser}] ]></ToUserName>
        <FromUserName>< ![CDATA[{fromUser}] ]></FromUserName>
        <CreateTime>{createTime}</CreateTime>
        <MsgType>< ![CDATA[image] ]></MsgType>
        <Image>
           <MediaId>< ![CDATA[{mediaId}] ]></MediaId>
        </Image>
        </xml>
        '''

##################################################语音消息#######################################################
class voiceMsg(object):
    def __init__(self, fromUserName, toUserName,text):
        self.fromUserName = fromUserName
        self.toUserName = toUserName
        self.text = text

    def xmlFormat(self):
        resultStr = '''
        <xml>
        <ToUserName>< ![CDATA[{toUser}] ]></ToUserName>
        <FromUserName>< ![CDATA[{fromUser}] ]></FromUserName>
        <CreateTime>{createTime}</CreateTime>
        <MsgType>< ![CDATA[voice] ]></MsgType>
        <Voice>
           <MediaId>< ![CDATA[{mediaId}] ]></MediaId>
        </Voice>
        </xml>
        '''

##################################################视频消息#######################################################
class videoMsg(object):
    def __init__(self, fromUserName, toUserName,text):
        self.fromUserName = fromUserName
        self.toUserName = toUserName
        self.text = text

    def xmlFormat(self):
        resultStr = '''
        <xml>
        <ToUserName>< ![CDATA[{toUser}] ]></ToUserName>
        <FromUserName>< ![CDATA[{fromUser}] ]></FromUserName>
        <CreateTime>{createTime}</CreateTime>
        <MsgType>< ![CDATA[video] ]></MsgType>
        <Video>
            <MediaId>< ![{mediaId}] ]></MediaId>
            <Title>< ![CDATA[{title}] ]></Title>
            <Description>< ![CDATA[{description}] ]></Description>
        </Video>
        </xml>
        '''

##################################################音乐消息#######################################################
class musicMsg(object):
    def __init__(self, fromUserName, toUserName,text):
        self.fromUserName = fromUserName
        self.toUserName = toUserName
        self.text = text

    def xmlFormat(self):
        resultStr = '''
        <xml>
        <ToUserName>< ![CDATA[toUser] ]></ToUserName>
        <FromUserName>< ![CDATA[fromUser] ]></FromUserName>
        <CreateTime>12345678</CreateTime>
        <MsgType>< ![CDATA[music] ]></MsgType>
        <Music>
            <Title>< ![CDATA[TITLE] ]></Title>
            <Description>< ![CDATA[DESCRIPTION] ]></Description>
            <MusicUrl>< ![CDATA[MUSIC_Url] ]></MusicUrl>
            <HQMusicUrl>< ![CDATA[HQ_MUSIC_Url] ]></HQMusicUrl>
            <ThumbMediaId>< ![CDATA[media_id] ]></ThumbMediaId>
        </Music>
        </xml>
        '''

##################################################图文消息#######################################################
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
