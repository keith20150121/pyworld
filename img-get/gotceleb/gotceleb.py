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
    return os.path.dirname(os.path.realpath(__file__)) + os.path.sep

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

class Fetch:
    def __init__(self):
        self.keywords = get_keyword(current() + 'keyword-list.txt')
        #self.homePage = 'http://www.baidu.com'
        self.homePage = 'http://www.gotceleb.com/?s='
        print('gotceleb.Fetch init done')
        
    def second(self, url, path):
        crawler, utl = self.crawler.local()
        content = crawler.visit(url)
        #utl.write(content, current() + 'text.xml')
        key = ' class="gallery-item">'
        #key = 'gallery-item'
        #if -1 == content.find(key):
        #    key = " class='gallery-item'>"
        urls, protos = utl.extractLinks(content, key, 'href="')
        if None is urls:
            print('extractLinks return None??')
            key = " class='gallery-item'>"
            urls, protos = utl.extractLinks(content, key, 'href="')
            if None is urls:
                print('extractLinks return None again?')
                return
        print('OK3')
        for url in urls:
            self.third(url, path)

    def third(self, url, path):
        crawler, utl = self.crawler.local()
        
        content = crawler.visit(url)
        tag = 'attachment type-attachment status-inherit hentry"'
        pic = utl.findLinkAfterTag(content, 'href="', tag)
        if None == pic:
            print('pic not found? NG4')
            return
        print('OK4')
        content = crawler.visit(pic)
        pic = utl.findLinkAfterTag(content, 'src="', tag)
        if None == pic:
            print('pic not found? NG5')
            return
        print('OK5')
        name = utl.getName(pic)
        if None is name:
            name = time.strftime('%Y%m%d%H%M%S.jpg', time.localtime(time.time()))
        else:
            name = utl.makePathName(name)

        path = path + name
        if os.path.exists(path) == True:
            path = path + time.strftime('%Y%m%d%H%M%S.jpg', time.localtime(time.time()))
        crawler.download(pic, path)
        
    def begin(self, crawler):
        utl = crawler.utl
        self.crawler = crawler
        for word in self.keywords:
            #crawler.visit('http://www.baidu.com')
            #crawler.visit('http://www.gotceleb.com')
            content = crawler.visit(self.homePage + word)
            #utl.write(content, current() + 'text.xml')
            #req = urlrequest.Request(url = self.homePage + word, headers = h)
            #res = crawler.visit(req)
            #content = crawler.read(res)
            urls, protos = utl.extractLinks(content, '<article ', 'href="')
            if None is urls:
                print('extractLinks return None??')
                return
            print('OK2')
            i = 0
            for url in urls:
                title = utl.findLink(protos[i], 'title="', 0)
                title = utl.makePathName(title)
                if None is not title:
                    path = current() + title + os.path.sep
                    if os.path.exists(path) == False:
                        os.mkdir(path)
                else:
                    print('title is None?')
                self.second(url, path)
                i = i + 1
            #print(res.read())
        
        
        
