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

def read(file_path):
    f = open(file_path, 'r')
    content = f.read()
    f.close()
    return content

def get_keyword(file_name):
    content = read(current() + file_name)
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

def toInt(a, default):
    if None is a:
        a = default
    else:
        try:
            a = int(a)
        except Exception as e:
            a = default
    return a

def get_information(file_name):
    content = read(current() + file_name)
    objs = json.loads(content)
    beg = objs['from']
    end = objs['to']
    return (toInt(beg, 1), toInt(end, 1))


class fw:
    def __init__(self, path):
        self.f = open(path, 'w', encoding='utf-8')
    def close(self):
        self.f.close()
    def dump(self, sth):
        self.f.flush()
        self.f.write(sth + '\n')

class Fetch:
    def __init__(self):
        self.keywords = get_keyword('keyword-list.txt')
        self.beginPage, self.endPage = get_information('config.json')
        #self.homePage = 'http://www.baidu.com'
        self.homePage = 'http://www.gotceleb.com/?s='
        self.multiPage = 'http://www.gotceleb.com/page/%d?s=%s'
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
        print('OK3, create download url list.')
        f = fw(path + 'urls.txt')
        for url in urls:
            pic = self.third(url, path)
            if None is not pic:
                f.dump(pic)
        f.close()

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
        if None is name or 250 < len(path + name):
            name = time.strftime('%H%M%S', time.localtime(time.time()))
            name = '%s%d%s.' % (name, random.randint(56, 8920), 'jpg')
        else:
            name = utl.makePathName(name)

        path = path + name
        if os.path.exists(path) == True:
            path = path + time.strftime('%Y%m%d%H%M%S.jpg', time.localtime(time.time()))       
        #crawler.download(pic, path)
        #crawler.mission.push(pic, path)
        self.download(crawler, pic, path)
        return pic

    def first(self, content, page):
        crawler, utl = self.crawler.local()
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

    @staticmethod
    def callWorkThread(crawler, pic, path):
        crawler.mission.push(pic, path)

    @staticmethod
    def doItMyself(crawler, pic, path):
        crawler.download(pic, path)        
    
    def begin(self, crawler):
        utl = crawler.utl
        self.crawler = crawler
        self.pages = 1
        self.download = Fetch.callWorkThread if crawler.mission is not None else Fetch.doItMyself
        for word in self.keywords:
            previous = self.homePage + word
            content = crawler.visit(previous)
            pages = utl.extractTagContent(content, '<span class="pages">', '</span>')
            if None is not pages:
                pages = re.sub(u'[^0-9]', '', pages)
                if None is not pages and 2 <= len(pages):
                    self.pages = int(pages[1:])
                    print('total pages:' + str(self.pages))
                else:
                    print('only 1 page.')
            else:
                print('extrace pages failed. only 1 page.')

            if None is not self.beginPage and self.beginPage > self.pages:
                print('begin page is out of range:' + str(self.pages))
                return

            page = self.beginPage
            end = self.endPage if self.endPage is not None and self.endPage > page else self.pages
            if page > 1:
                h = utl.headers({
                    'Referer' : previous
                    })
                print(h)
                previous = self.multiPage % (page, word)
                content = crawler.visitWithHeader(previous, h)                
            while True:
                print('begin page:' + str(page))
                self.first(content, page)
                page = page + 1
                if page <= end:#self.pages:
                    h = utl.headers({'Referer' : previous})
                    previous = self.multiPage % (page, word)
                    content = crawler.visitWithHeader(previous, h)
                else:
                    break;
        
        
        
