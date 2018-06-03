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
    return os.path.dirname(os.path.realpath(__file__)) + '/'
    
class ImgCrawler:
    def __init__(self):
        cookieJar = http.cookiejar.CookieJar()
        handler = urlrequest.HTTPCookieProcessor(cookieJar)
        self.opener = urlrequest.build_opener(handler)

    def assign(self, fetcher):
        self.fetcher = fetcher

    def visit(self, url):
        print('visit:' + url)
        return self.visitWithHeader(url, ImgCrawler.getHeaders())
        
    def visitWithHeader(self, url, h):
        req = urlrequest.Request(url = url, headers = h)
        content = None
        for i in range(8):
            try:
                res = self.opener.open(req, timeout = 30)
                #b = res.read()
                #content = b.decode('utf8', 'ignore')
                print('about to read')
                #print(b)
                content = self.read(res)
                #print(content)
            except Exception as e:
                print(e)
                print('!!!!!!!!!!!!!!!!!!!!!!!!!!!try more %d times' % (7 - i))
        
        print('return content')
        return content

    @staticmethod
    def read(res):
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
            
        '''
        try:
            ppu = u.encode('gbk', 'ignore')
            print(ppu)
        except Exception as e:
            print(e)
        '''
            
        return u

    @staticmethod
    def getHeaders():
        h = {
            'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0',
            'Accept-Language' : 'en-US,en;q=0.5',
            'Connection' : 'keep-alive',
            'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding' : "gzip, deflate",
            'Accept-Language' : 'en-US,en;q=0.5',
            'Upgrad-Insecure-Request' : '1'
        }
        return h

    @staticmethod
    def headers(update):
        h = {
            'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0',
            'Accept-Language' : 'en-US,en;q=0.5',
            'Connection' : 'keep-alive',
        }
        h.update(update)
        return h

    @staticmethod
    def detectEncoding(res):
        header = res.getheader('Content-Type').lower()
        return header[header.find('charset=') + len('charset='):]

    def write(self, b, path):
        #if os.path.exists(path) == False:
        #    os.mkdir(path)
        f = open(path, 'wb')
        f.write(b)
        f.flush()
        f.close()
        
    def download(self, url, path):
        req = urlrequest.Request(url = url, headers = ImgCrawler.getHeaders())
        b = self.opener.open(req).read()
        self.write(b, path)

def fetch_web_objects(webs):
    cur = current()
    f = open(cur + webs, 'r')
    objs = json.loads(f.read())#, encoding="UTF8")
    f.close()
    return (objs.keys())
    

def get_keyword(keyword):
    f = open(current() + keyword, 'r')
    keywords = f.read()
    print(keywords)
    f.close()
    return keywords

def main():
    crawler = ImgCrawler()
    fetchers = fetch_web_objects('webs.json')
    objs = []
    for fetcher in fetchers:
        exec('from %s import %s' % (fetcher, fetcher))
        obj = eval('%s.Fetch()' % (fetcher))

        obj.begin(crawler)
        
        objs.append(obj)
        
        
if __name__ == '__main__':
    main()
