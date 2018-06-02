import http.cookiejar
import urllib
import urllib.request
import urllib.parse
import re
import sys
import time
import os
import json
import http.client

if sys.version.find('3') == 0:
    import urllib.request
    urlrequest = urllib.request
    urlparse = urllib.parse
else:
    import urllib2
    urlrequest = urllib2
    urlparse = urllib

if __name__ == '__main__':
    print('gotceleb do nothing as main')

def current():
    return os.path.dirname(os.path.realpath(__file__)) + '/'

def get_keyword(file_path):
    f = open(file_path, 'r')
    content = f.read()
    f.close()
    keywords = content.split(',')
    ret = []
    for word in keywords:
        word = word.strip('\u0020\u3000\n')
        ret.append(re.sub('[\u3000|\u0020]+', '+', word))

    last = ret[-1]
    if None is last or 0 == len(last):
        ret.remove(last)
        
    print(ret)
    return ret

def findLink(content, key, beg):
    beg = content.find(key, beg)
    if -1 == beg:
        print('beg is -1?')
        return
    beg = beg + len(key)
    end = content.find('"', beg)
    if -1 == end:
        print('end is -1?')
        return
    return content[beg:end]

def findHref(content, beg):
    return findLink(content, 'href="', beg)

def findSrc(content, beg):
    return findLink(content, 'src="', beg)

def getName(url):
    beg = url.rfind('/')
    return url[beg:]

class Fetch:
    def __init__(self):
        self.keywords = get_keyword(current() + 'keyword-list.txt')
        #self.homePage = 'http://www.baidu.com'
        self.homePage = 'http://www.gotceleb.com/?s='
        print('gotceleb.Fetch init')

    def common(self, url, h):
        crawler = self.crawler
        print(url)
        req = urlrequest.Request(url = url, headers = h)
        content = crawler.read(crawler.visit(req))
        return content

    def second(self, url, h):
        content = self.common(url, h)

        '''
        key = 'class="attachment-medium size-medium"'
        beg = content.find(key)
        pic = findSrc(content, beg + len(key))
        req = urlrequest.Request(url = pic, headers = h)
        print('ok4')
        crawler.download(req, current() + getName(pic))
        '''
        key = 'class="gallery-icon portrait"'
        bigs = content.split(key)
        print('OK3')

        ret = []
        for big in bigs:
            url = findHref(big, 0)
            if None is url:
                print('href url is None? NG3-1.')
                continue
            ret.append(url)

        return ret

    def third(self, url, h):
        crawler = self.crawler
        content = self.common(url, h)
        key = 'class="attachment-medium size-medium"'
        beg = content.find(key)
        pic = findSrc(content, beg + len(key))
        if None is pic:
            print('pic is None? NG4')
            return
        req = urlrequest.Request(url = pic, headers = h)
        print('OK4')
        crawler.download(req, current() + getName(pic))
        
    def begin(self, crawler):
        self.crawler = crawler
        for word in self.keywords:
            h = crawler.getHeaders()
            content = self.common(self.homePage + word, h)
            #req = urlrequest.Request(url = self.homePage + word, headers = h)
            #res = crawler.visit(req)
            #content = crawler.read(res)
            articles = content.split('article')
            print('OK2')
            for article in articles:
                url = findHref(article, 0)
                if None is url:
                    continue
                req = urlrequest.Request(url = url, headers = h)
                content = crawler.read(crawler.visit(req))
                bigs = self.second(crawler, url, h)
                for big in bigs:
                    self.third(big, h)
                
            #print(res.read())        
        
        
        
