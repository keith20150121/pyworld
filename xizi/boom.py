#!/usr/bin/python

import http.cookiejar
import urllib
import urllib.request
import re
import sys
import time
import os
import json
import base64


#suid = 'XZGUEST-6DB0F831-6C3F-AF23-7C7F-E9F9AB0DB41B'
#COOKIE = 'UM_distinctid=15aea2a04c2817-0c67d7258ecae5-75256750-1aeaa0-15aea2a04c311cb; PHPSESSID=mqkt7tjp5a2u72clitvn7vflu5; CNZZDATA4510143=cnzz_eid%3D1249694494-1498614319-http%253A%252F%252Fbbs.xizi.com%252F%26ntime%3D1498795776; CNZZDATA1254803729=839662550-1498615804-http%253A%252F%252Fbbs.xizi.com%252F%7C1498797260; Xz_suid=XZGUEST-6DB0F831-6C3F-AF23-7C7F-E9F9AB0DB41B'

def passCaptcha(cookieJar, opener, ssid):
    verifyCodeUrl = 'http://my2.xizi.com/api/safety/captcha'
    response = opener.open(verifyCodeUrl)
    vcd = response.read()
    #phpSessId = ''
    #for cookie in cookieJar:
    #    print(cookie.domain, cookie.name, cookie.value)
    #    if cookie.domain == 'my2.xizi.com' and cookie.name == 'PHPSESSID':
    #        phpSessId = cookie.value

    # skip json parse.
    vcd = vcd[vcd.find(b',') + 1:]
    vcd = base64.decodebytes(vcd)

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

    #return phpSessId

def boomWithCookie(phone, times, COOKIE):
    times = int(times)
    cookieJar = http.cookiejar.CookieJar()
    handler = urllib.request.HTTPCookieProcessor(cookieJar)
    opener = urllib.request.build_opener(handler)
    
    boom = 'http://my2.xizi.com/api/member/check-phone'
    post = {
        'type' : 'new',
        'phone' : phone,
    }

    headers = {
        'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0',
        'X-Requested-With' : 'XMLHttpRequest',
        'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie' : COOKIE,
        'Connection' : 'keep-alive',
    }
    post = urllib.parse.urlencode(post).encode(encoding='UTF8')
    request = urllib.request.Request(boom, post, headers)

    while times >= 0:
        response = json.loads(str(opener.open(request).read(), 'utf-8'))
        if response['code'] == 10031:
            print('No more retry received from Xizi.')
            return
        
        print(response)
        print('times=' + str(times))
        time.sleep(60)
        times -= 1
    

def post(opener, url, headers, data):
    data = urllib.parse.urlencode(data).encode(encoding='UTF8')
    request = urllib.request.Request(url, data, headers)
    return request

def boomFromXiziEntry(phone, times):
    times = int(times)
    if times <= 0:
        print('times <= 0!')
        return


    cookieJar = http.cookiejar.CookieJar()
    handler = urllib.request.HTTPCookieProcessor(cookieJar)
    opener = urllib.request.build_opener(handler)

    #opener.addheaders = [
    #    ('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0'),
    #    ('Refer', 'http://my2.xizi.com/user/sign')]

    headers = {
        'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0',
        'Refer' : 'http://my2.xizi.com/user/sign'
    }

    xizi = 'http://my2.xizi.com/user/sign'
    request = urllib.request.Request(
        url = xizi,
        headers = headers)
    response = opener.open(request)
    print(cookieJar)
    #-----------------------cookieJar:PHPSESSID, Xz_suid----------------------------------
    phpSessId, suid = '', ''
    for cookie in cookieJar:
        if cookie.domain.find('xizi') >= 0:
            if cookie.name == 'PHPSESSID':
                phpSessId = cookie.value
            elif cookie.name == 'Xz_suid':
                suid = cookie.value

    if phpSessId == '' or suid == '':
        print('session or suid is null!')
        return
    
    style = 'http://my2.xizi.com/js/style.js' 

    request = urllib.request.Request(
        url = style,
        headers = headers)
    response = opener.open(request)
    page = response.read()
    #print(page)
    #print(cookieJar)
    beg = page.find(b"ssid = '") + 8
    ssid = page[beg : page.find(b"'", beg)]
    print(ssid)
    #-----------------------------ssid----------------------------------------------
    s = '{"ua":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTM\
ko) Chrome/49.0.2623.75 Safari/537.36 LBBROWSER","sys":"Win32","lan":\
okie":true,"cliview":[791,733],"scrview":[768,1366],"color":24,"ref":\
.xizi.com/","ssid":"' + str(ssid, 'utf-8') + '","suid":"' + suid + '"}'
    print(s)
    s = str(base64.b64encode(s.encode('ascii')), 'utf-8').replace('=', '')    
    url = 'http://my2.xizi.com/api/safety/analyze?s=' + s
    #print(url)
    request = urllib.request.Request(
        url = url,
        headers = headers)
    response = opener.open(request)
    result = json.loads(str(response.read(), 'utf-8'))

    phpSessId = ''
    if result['code'] == 403:
        passCaptcha(cookieJar, opener, ssid)
    #---------------------? still 403 but can pass captcha for now----------------------------
    vc = input('Please input the verify code:')
    captcha_check = 'http://my2.xizi.com/api/safety/captcha-check?code=' + vc
    
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0',
        'Refer' : 'http://my2.xizi.com/user/sign',
    }

    #if phpSessId != '':
    #    headers['Cookie'] = 'PHPSESSID=' + phpSessId
    
    request = urllib.request.Request(
        url = captcha_check,
        headers = headers)
    result = json.loads(str(opener.open(request).read(), 'utf-8'))
    print(result)
    #if result['code'] != 200:
    #    print('captcha check failed!')
    #    return
    #----------------------Pass captcha-------------------------
    check = 'http://my2.xizi.com/api/member/login-check'
    post = {
        'username' : phone,
        'u' : s,
    }
    post = urllib.parse.urlencode(post).encode(encoding='UTF8')
    request = urllib.request.Request(check, post, headers)
    response = opener.open(request).read()
    print(response)
    #----------------------log-check-----------------------------
    boom = 'http://my2.xizi.com/api/member/check-phone'
    post = {
        'type' : 'new',
        'phone' : phone,
    }
    post = urllib.parse.urlencode(post).encode(encoding='UTF8')
    request = urllib.request.Request(boom, post, headers)

    while times >= 0:
        response = json.loads(str(opener.open(request).read(), 'utf-8'))
        print(response)
        print('times=' + str(times))
        time.sleep(60)
        times -= 1
    #------------------------SendSms------------------------------
if __name__ == '__main__':
    print('phone=' + sys.argv[1] + ', times=' + sys.argv[2])
    boomFromXiziEntry(sys.argv[1], sys.argv[2])
    #boomWithCookie(sys.argv[1], sys.argv[2], sys.argv[3])

