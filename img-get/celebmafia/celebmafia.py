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
from urllib import parse

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

def get_information(utl, file_name):
    content = read(current() + file_name)
    objs = json.loads(content)
    beg = objs['from']
    end = objs['to']
    return (utl.toInt(beg, 1), utl.toInt(end, 1))

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
        self.homePage = 'http://celebmafia.com/search/?q='
        #self.multiPage = 'http://celebmafia.com/search/?_siq_page=%d&_siq_sort=newest&q=%s'
        print('celebmafia.Fetch init done')

    def second(self, url, path):
        crawler, utl = self.crawler.local()
        content = crawler.visit(url)
        key = '<div class="image-box">'
        urls, protos = utl.extractLinks(content, key, 'href="')
        if urls is None:
            print('error!!!!!!')
            return
        print('OK3, create download url list.')
        f = fw(path + 'urls.txt')
        for url in urls:
            name = utl.getName(url)
            if None is name or 250 < len(path + name):
                name = time.strftime('%H%M%S', time.localtime(time.time()))
                name = '%s%d%s.' % (name, random.randint(56, 8920), 'jpg')
            else:
                name = utl.makePathName(name)
            if None is not url:
                f.dump(url)
                self.download(crawler, url, path + name)
            else:
                print('url is None?')
        f.close()

    def first(self, l):
        for p in l:
            title = p.title
            url = p.url
            if title is None:
                print('get title failed')
                title = time.strftime('%H%M%S', time.localtime(time.time()))

            path = current() + title + os.path.sep
            if os.path.exists(path) == False:
                os.mkdir(path)

            self.second(url, path)

    @staticmethod
    def callWorkThread(crawler, pic, path):
        crawler.mission.push(pic, path)

    @staticmethod
    def doItMyself(crawler, pic, path):
        crawler.download(pic, path)        


    class Pairs:
        def __init__(self, url, title):
            self.url = url
            self.title = title

    def fetch(self, content, l):
        j = (json.loads(content))['main']
        records = j['records']
        if None is records or type(records) is not type([]):
            print('No records in response from:' + url)
            return l
        
        for a in records:
            title = re.sub('<em>|</em>', '', a['title'])
            title = self.crawler.utl.makePathName(title)
            l.append(Fetch.Pairs(a['url'], title))

        return l

    def search(self, content, keyword, previous):
        crawler, utl = self.crawler.local()
        engineKey = utl.findLinkAfterTag(content, '"', 'engineKey:')
        #print('ek:' + engineKey)
        each = 20
        pattern = '"http://api.searchiq.co/api/search/results?q=%s&engineKey=%s&page=%d&itemsPerPage=%d&group=0&sortby=newest&autocomplete=0"'
        url = pattern % (parse.quote(keyword), engineKey, self.beginPage, each)
        h = utl.headers({
            'Referer' : previous,
            'Accept' : 'application/json, text/javascript, */*; q=0.01',
            'Origin' : 'http://celebmafia.com'            
            })
        content = crawler.visitWithHeader(url, h)
        #urls, protos = utl.extractLinks(content, '"url"', '"')
        j = (json.loads(content))['main']
        records = j['records']
        if None is records or type(records) is not type([]):
            print('No records in response from:' + url)
            return

        total = j['totalResults']
        print('===>>>> total : ' + str(total))
        ret = []
        for a in records:
            title = re.sub('<em>|</em>', '', a['title'])
            title = self.crawler.utl.makePathName(title)
            ret.append(Fetch.Pairs(a['url'], title))

        if total <= each:
            return ret

        page = self.beginPage + 1
        for b in range(each, total, each):
            if page > self.endPage:
                break
            url = pattern % (parse.quote(keyword), engineKey, page, each)
            content = crawler.visitWithHeader(url, h)
            self.fetch(content, ret)
            page = page + 1

        return ret
        
    def begin(self, crawler):
        utl = crawler.utl
        self.crawler = crawler
        self.keywords = get_keyword('keyword-list.txt')
        self.beginPage, self.endPage = get_information(utl, 'config.json')        
        self.pages = 1
        self.download = Fetch.callWorkThread if crawler.mission is not None else Fetch.doItMyself
        for word in self.keywords:
            previous = self.homePage + word
            content = crawler.visit(previous)
            l = self.search(content, word, previous)
            self.first(l)
            
