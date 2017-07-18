# -*- coding: UTF-8 –*- 
#!/usr/bin/python

import http.cookiejar
import urllib
import urllib.request
import re
import sys
import time
import os
import json
import itchat
from itchat.content import *

class TulingRobot:
    def __init__(self, opener):
        self.opener = opener
        # access tap for cookies, userid
        self.id = self.getUserId()

    def getUserId(self):
        content = self.opener.open('http://www.tuling123.com/experience/exp_virtual_robot.jhtml?nav=exp').read().decode('utf8', 'ignore')
        key = 'window.localStorage.setItem("_userid", ' + "'"
        id_beg = content.find(key) + len(key)
        id_end = content.find("'", id_beg)
        i = content[id_beg : id_end]
        print('userid=' + i)
        return i

    def chat(self, info):
        #post = {
        #    'info' : info,
        #    'userid' : self.id,
        #    '_xsrf' : '',
        #}
        post = {
            'key': 'bec269facd1e4365a826bedbde78d720',
            'info' : info,
            'userid' : 'wechat-robot', #+ self.id
        }
        post = urllib.parse.urlencode(post).encode(encoding='UTF8')
        request = urllib.request.Request('http://www.tuling123.com/openapi/api', post)
        #request = urllib.request.Request('http://www.tuling123.com/api/product_exper/chat.jhtml', post)
        #response = self.opener.open(request, timeout = 2).read().decode('utf8')
        response = request_all_the_time(self.opener, request, 5).read().decode('utf8', 'ignore')
        #key = '<Content><![CDATA['
        #l = len(key)
        #beg = response.find(key) + l
        #end = response.find("]", beg)
        #ret = response[beg : end]
        ret = json.loads(response)
        print('TULING: ' + ret['text'])
        return ret['text']

class SimsimiRobot:    
    def __init__(self, opener):
        self.opener = opener
        # access tap for cookies, userid
        #self.id = self.getUserId()

    def warmUp(self):
        content = self.opener.open('http://www.niurenqushi.com/app/simsimi/').read().decode('utf8', 'ignore')

    def chat(self, info):
        post = {
            'txt' : info.encode('utf-8'),
        }
        post = urllib.parse.urlencode(post).encode(encoding='UTF8')
        request = urllib.request.Request('http://www.niurenqushi.com/api/simsimi/', post)
        response = json.loads(request_all_the_time(self.opener, request, 5).read().decode('utf8', 'ignore'))
        ret = response['text']
        print('SIMSIMI: ' + ret)
        return ret 


class WechatIce:
    def __init__(self, other_robot):
        self.other = other_robot

        #@itchat.msg_register(itchat.content.TEXT, isMpChat = True)
        @itchat.msg_register(TEXT, isMpChat = True)
        def text_reply(msg):
            try:
                print('%s:%s'% ('Ice', msg.text))
            except Exception as e:
                print('Ice: wrong coded.')
            msg.user.send(self.other.chat(msg.text))
            #if msg['FromUserName'] == 'xiaoice-ms':
            #    return self.other.chat(msg.text)

        @itchat.msg_register([PICTURE, RECORDING], isMpChat = True)
        def non_text_reply(msg):
            print('Ice: [non-text]')
            msg.user.send('语音或者图片在上班时间我不方便打开啊~发文字信息吧！')
        
        
        itchat.auto_login(hotReload = True)
        self.ice = itchat.search_mps('小冰')[0]

    def __del__(self):
        itchat.logout()

    def chat(self, info):
        print('Ice:' + info)
        self.ice.send(info)

    def run(self):
        itchat.run()
        

def request_all_the_time(opener, request, timeout):
    try:
        ret = opener.open(request, timeout = timeout)
    except Exception as e:
        print(e)
        return request_all_the_time(opener, request, timeout)
    return ret

def ask_answer_loop(ask, answer, info):
    while True:
        info = ask.chat(info)
        info = answer.chat(info)
        print('')
        #time.sleep(0.5)
        

def robotChat(aa, info):
    aa = int(aa)
    
    # network
    cookieJar = http.cookiejar.CookieJar()
    handler = urllib.request.HTTPCookieProcessor(cookieJar)
    opener = urllib.request.build_opener(handler)
    # robots definition
    tuling = TulingRobot(opener)
    simsimi = SimsimiRobot(opener)

    if aa == 1:
        ask = tuling
        answer = simsimi
    else:
        ask = simsimi
        answer = tuling

    ask_answer_loop(ask, answer, info)

def talk2Wechat():
    # network
    cookieJar = http.cookiejar.CookieJar()
    handler = urllib.request.HTTPCookieProcessor(cookieJar)
    opener = urllib.request.build_opener(handler)
    # robots definition
    tuling = TulingRobot(opener)
    wechat = WechatIce(tuling)
    wechat.chat(sys.argv[1])
    wechat.run()

if __name__ == '__main__':
    #robotChat(sys.argv[1], sys.argv[2])
    talk2Wechat()

