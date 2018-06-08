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
        self.homePage = 'http://celebmafia.com/search/?q='
        self.multiPage = 'http://celebmafia.com/search/?_siq_page=%d&_siq_sort=newest&q=%s'
        print('celebmafia.Fetch init done')

    def second(self, url, path):
        crawler, utl = self.crawler.local()
        content = crawler.visit(url)
        key = '<div class="image-box">'
        urls, protos = utl.extractLinks(content, key, 'href="')
        print('OK3, create download url list.')
        f = fw(path + 'urls.txt')
        for url in urls:
            if None is not url:
                f.dump(url)
                self.download(crawler, url, path)
            else:
                print('url is None?')
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
        urls, protos = utl.extractLinks(content, '<a class="siq-partner-result" ', 'href="')
        if None is urls:
            print('extractLinks return None??')
            return
        print('OK2')
        i = 0
        for url in urls:
            title = utl.extractTagContent(protos[i], '>', '</a>', 0)
            if title is not None:
                title = re.sub('<em>|</em>', '', title)
                title = utl.makePathName(title)
            else:
                print('get title failed')
                title = time.strftime('%H%M%S', time.localtime(time.time()))
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
            pages = utl.extractTagContent(content, '<a class="_siq_pagination_single_link"', '</a>')
            beg = pages.rfind('>')
            if -1 == beg:
                print('get pages failed, set page(s) = 1')
                pages = 1
            else:
                pages = pages[pages.rfind('>') + 1:]
                pages = toInt(pages, 1)

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
        
        
        
