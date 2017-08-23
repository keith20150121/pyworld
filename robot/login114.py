#!/usr/bin/python

import sys

if sys.version.find('3') == 0:
    import urllib.request
    urlrequest = urllib.request
else:
    import urllib2
    urlrequest = urllib2

import cookielib
import urllib
import re
import time
import os
import json
import base64

def request_all_the_time(opener, request, timeout):
    try:
        ret = opener.open(request, timeout = timeout)
    except Exception as e:
        print(e)
        return request_all_the_time(opener, request, timeout)
    return ret

def login_until_failure(interval):

    accounts = [
        {
            'username' : '17010071418',
            'password' : '4229',
        },
        {
            'username' : '13610444560',
            'password' : '9106',
        },
        {
            'username' : '15992659973',
            'password' : '6091',
        },
        {
            'username' : '18688340675',
            'password' : '8336',
        },
        {
            'username' : '13829954067',
            'password' : '5839',
        },
    ]

    size = len(accounts)
    i = 0
    err = 0

    cookieJar = cookielib.CookieJar()
    handler = urlrequest.HTTPCookieProcessor(cookieJar)
    opener = urlrequest.build_opener(handler)
    url = 'http://wifi.gd118114.cn/login.ajax'
    post = urllib.urlencode(accounts[i])

    while True:        
        req = urlrequest.Request(url, post)
        res = json.loads(request_all_the_time(opener, req, 5).read())
        print(res)

        if res['resultCode'] != u'0':
            if err < 3:
                err += 1
                time.sleep(2)
                continue
            if i + 1 < size:
                i += 1
                err = 0
                post = urllib.urlencode(accounts[i])
                continue
            else:
                print('i > size, exit.')
                break

        time.sleep(interval)

if __name__ == '__main__':
    login_until_failure(int(sys.argv[1]))

