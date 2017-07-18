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
        post = {
            'info' : info,
            'userid' : self.id,
            '_xsrf' : '',
        }
        post = urllib.parse.urlencode(post).encode(encoding='UTF8')
        request = urllib.request.Request('http://www.tuling123.com/api/product_exper/chat.jhtml', post)
        #response = self.opener.open(request, timeout = 2).read().decode('utf8')
        response = request_all_the_time(self.opener, request, 5).read().decode('utf8', 'ignore')
        key = '<Content><![CDATA['
        l = len(key)
        beg = response.find(key) + l
        end = response.find("]", beg)
        ret = response[beg : end]
        try:
            print('TULING: ' + ret)
        except Exception as e:
            print(e)
        return ret

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
        try:
            print('SIMSIMI: ' + ret)
        except Exception as e:
            print(e)
        return ret 

def request_all_the_time(opener, request, timeout):
    try:
        ret = opener.open(request, timeout = timeout)
    except Exception as e:
        print(e)
        return request_all_the_time(opener, request, timeout)
    return ret

def max_repeat(str1, str2):
    l1 = len(str1)
    l2 = len(str2)
    if l1 >= l2:
        long = str1
        short = str2
        len_long = l1
        len_short = l2
    else:
        long = str2
        short = str1
        len_long = l2
        len_short = l1

    MAX = 0
    for i in range(len_long):
        j = i + 1
        while j <= len_long:
            sub = long[i:j]
            if short.find(sub) < 0:
                break
            elif j - i > MAX:
                MAX = j - i
                if MAX == len_short:
                    return (MAX, len_short)
            j += 1
    return (MAX, len_short)

class ConvergenceDefencer:
    def __init__(self, ask, answer):
        self.ask = ask
        self.answer = answer
        self.convergenceFile = open('%s/%d-%s' % (sys.path[0], time.time(), 'convergence.txt'), 'w')
        self.log = open('%s/%d-%s' % (sys.path[0], time.time(), 'log.txt'), 'w')

    def loop(self, info1, sleep = 0):
        try:
            while True:
                self.log.writelines([info1, '\n'])
                info2 = self.ask.chat(info1)
                self.log.writelines([info2, '\n\n'])
                info3 = self.answer.chat(info2)
                info1 = info3
                print('')
                repeat_1_2 = max_repeat(info1, info2)
                #print(repeat_1_2)
                if repeat_1_2[0] == 0:
                    continue
                repeat_2_3 = max_repeat(info2, info3)
                #print(repeat_2_3)
                if repeat_2_3[0] == 0:
                    continue
                if repeat_1_2[1] * 0.8 <= repeat_1_2[0] and repeat_2_3[1] * 0.8 <= repeat_2_3[0]:
                    print('[system] : answer repeated!')
                    print(repeat_1_2)
                    print(repeat_2_3)
                    self.convergenceFile.writelines([info1, '\n', info2, '\n',  info3, '\n\n'])
                    info1 = '为什么又重复我说的话，给点心聊天好吗？'

                time.sleep(sleep)
        finally:
             self.convergenceFile.close()
             self.log.close()

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

    #ask_answer_loop(ask, answer, info)
    con = ConvergenceDefencer(ask, answer)
    con.loop(info)

if __name__ == '__main__':
    robotChat(sys.argv[1], sys.argv[2])

