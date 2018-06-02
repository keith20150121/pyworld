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
import http.client

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

def current():
    return sys.path[0] + '/'
    
class ImgCrawler:
    def __init__(self):
        cookieJar = http.cookiejar.CookieJar()
        handler = urlrequest.HTTPCookieProcessor(cookieJar)
        self.opener = urlrequest.build_opener(handler)

    def setCore(self, core):
        self.core = core

    @staticmethod
    def headers(update):
        h = {
            'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0',
            'Accept-Language' : 'en-US,en;q=0.5',
            'Connection' : 'keep-alive',
        }
        h.update(update)
        return h

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

def fetch_web_objects(webs):
    cur = current()
    f = open(cur + webs, 'r')
    objs = json.loads(f.read())#, encoding="UTF8")
    print(objs.keys())
    f.close()

def get_keyword(keyword):
    f = open(current() + keyword, 'r')
    keywords = f.read()
    print(keywords)
    f.close()
    return keywords

if __name__ == '__main__':
    fetch_web_objects('webs.json')
    print(get_keyword('gotceleb/keyword-list.txt').split(','))
