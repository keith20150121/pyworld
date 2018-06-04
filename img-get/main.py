import http.cookiejar
import urllib
import urllib.request
import urllib.parse
import re
import sys
import time
import os, shutil
import json
import random
import http.client
import codecs

if sys.version.find('3') == 0:
    import urllib.request
    urlrequest = urllib.request
    urlparse = urllib.parse
else:
    import urllib2
    urlrequest = urllib2
    urlparse = urllib

def current():
    return os.path.dirname(os.path.realpath(__file__)) + os.path.sep

class Utl:
    @staticmethod
    def makePathName(name):
        return re.sub(u'[^\u4e00-\u9fa5_.a-zA-Z0-9]', '_', name)
    
    @staticmethod
    def findLink(content, key, beg, quo = '"'):
        beg = content.find(key, beg)
        if -1 == beg:
            print('beg is -1?')
            return
        beg = beg + len(key)
        end = content.find(quo, beg)#'"', beg)
        if -1 == end:
            print('end is -1?')
            return
        return content[beg:end]

    @staticmethod
    def extractLinks(content, split_key, link_key, quo = '"', tryQuo = True):
        protos = content.split(split_key)
        print('extractLinks by %s, %s, size:%d' % (split_key, link_key, len(protos)))
        if None is not protos and 1 < len(protos):
            protos.pop(0)
        else:
            if False == tryQuo:
                print('No or not enough %s in content?' % (split_key))
                return (None, None)
            if quo == '"':
                quo = "'"
                split_key = split_key.replace('"', quo)
                link_key = link_key.replace('"', quo)
            else:
                quo = '"'
                split_key = split_key.replace("'", quo)
                link_key = link_key.replace("'", quo)
            return Utl.extractLinks(content, split_key, link_key, quo, False)
        ret = []
        ma = []
        i = 0
        for proto in protos:
            if proto == '':
                print('skip empty')
                continue
            #Utl.write(proto, current() + 'text.txt')
            url = Utl.findLink(proto, link_key, 0, quo)
            if None is url:
                print(proto)
                print('Not found link in proto?, ' + str(i))
            else:
                ret.append(url)
                ma.append(proto)
            i = i + 1
        return ret, ma

    @staticmethod
    def extractTagContent(content, prefix, postfix, quo = '"', tryQuo = True):
        beg = content.find(prefix)
        if -1 == beg:
            if -1 != prefix.find(quo) and True == tryQuo:
                if quo == '"':
                    prefix = prefix.replace(quo, "'")
                    postfix = postfix.replace(quo, "'")
                    return Utl.extractTagContent(content, prefix, postfix, "'", False)
            else:
                print('Not found ' + tag)
            return
        end = content.find(postfix, beg + len(prefix))
        if -1 == end:
            print('end is -1?')
            return
        return content[beg : end]

    @staticmethod
    def findLinkAfterTag(content, key, tag, quo = '"'):
        beg = content.find(tag)
        if -1 == beg:
            print('Not found ' + tag)
            return
        return Utl.findLink(content, key, beg, quo)

    @staticmethod
    def findHref(content, beg, quo = '"'):
        return findLink(content, 'href="', beg, quo)

    @staticmethod
    def findSrc(content, beg, quo = '"'):
        return findLink(content, 'src="', beg, quo)
    
    @staticmethod
    def getName(url):
        beg = url.rfind('/')
        if -1 == beg:
            return None
        return url[beg:]

    @staticmethod
    def write(b, path):
        #if os.path.exists(path) == False:
        #    os.mkdir(path)
        print('write:' + path)
        if isinstance(b, str):
            f = open(path, 'w', encoding='utf-8')
        else:
            f = open(path, 'wb')
        f.write(b)
        f.flush()
        f.close()

    @staticmethod
    def read(res):
        failed = True
        encode = Utl.detectEncoding(res)
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
            
        return u

    @staticmethod
    def getHeaders():
        h = {
            'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0',
            'Accept-Language' : 'en-US,en;q=0.5',
            'Connection' : 'keep-alive',
            'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language' : 'en-US,en;q=0.5',
            'Upgrad-Insecure-Request' : '1'
        }
        #   'Accept-Encoding' : "utf8",
        return h

    @staticmethod
    def headers(update):
        h = Utl.getHeaders()
        h.update(update)
        return h

    @staticmethod
    def detectEncoding(res):
        header = res.getheader('Content-Type').lower()
        return header[header.find('charset=') + len('charset='):]

class WgetCrawler:
    def __init__(self):
        self.tmp = current() + 'tmp' + os.path.sep
        if os.path.exists(self.tmp) == False:
            os.mkdir(self.tmp)
        self.utl = Utl

    def local(self):
        return (self, self.utl)

    def visit(self, url):
        return self.visitWithHeader(url, Utl.getHeaders())
        
    def visitWithHeader(self, url, h):
        print('visit:' + url)
        fileName = Utl.getName(url)
        dst = self.tmp + 'temp'
        os.system('wget -O %s --timeout=30 %s' % (dst, url))
        f = codecs.open(dst,'r','utf-8')
        #f = open(dst, 'r')
        content = f.read()
        f.close()
        os.remove(dst)
        return content
       
    def download(self, url, path):
        fileName = Utl.getName(url)
        os.system('wget -O %s %s ' % (path, url))
        
class HttpCrawler:
    def __init__(self):
        cookieJar = http.cookiejar.CookieJar()
        handler = urlrequest.HTTPCookieProcessor(cookieJar)
        self.opener = urlrequest.build_opener(handler)
        self.utl = Utl

    def local(self):
        return (self, self.utl)

    def visit(self, url):
        return self.visitWithHeader(url, Utl.getHeaders())
        
    def visitWithHeader(self, url, h):
        print('visit:' + url)
        req = urlrequest.Request(url = url, headers = h)
        content = None
        for i in range(8):
            try:
                res = self.opener.open(req, timeout = 40)
                #b = res.read()
                #content = b.decode('utf8', 'ignore')
                print('about to read')
                content = Utl.read(res)
                print('read done')
                break
            except Exception as e:
                print(e)
                print('!try more %d times' % (7 - i))
        
        print('return content')
        return content
       
    def download(self, url, path):
        req = urlrequest.Request(url = url, headers = Utl.getHeaders())
        for i in range(8):
            try:
                res = self.opener.open(req, timeout = 40)
                b = res.read()
                break
            except Exception as e:
                print(e)
                print('!try more %d times' % (7 - i))
                
        if None is not b:
            Utl.write(b, path)
        else:
            print('read() error')

def load_json(path):
    f = open(path, 'r')
    objs = json.loads(f.read())#, encoding="UTF8")
    f.close()
    return objs

def fetch_web_objects(webs):
    objs = load_json(current() + webs)
    return (objs.keys())

def decide_crawler(rule):
    objs = load_json(current() + rule)
    crawler = objs['crawler']
    if 'wget' == crawler:
        return WgetCrawler()
    if 'http' == crawler:
        return HttpCrawler()
    return

def main():
    crawler = decide_crawler('rule.json')
    fetchers = fetch_web_objects('webs.json')
    objs = []
    for fetcher in fetchers:
        exec('from %s import %s' % (fetcher, fetcher))
        obj = eval('%s.Fetch()' % (fetcher))

        obj.begin(crawler)
        
        objs.append(obj)
        
        
if __name__ == '__main__':
    main()
