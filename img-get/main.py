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

def get_keyword():
        p = sys.path[0] + '/' + 'keyword-list.txt'
        #print(p)
        f = open(sys.path[0] + '/' + 'keyword-list.txt', 'r')
        l = f.readline()
        keywords = ''
        while l:
                keywords = keywords + str(l)
                l = f.readline()
        #print(keywords)
        f.close()
        return keywords

if __name__ == '__main__':
        print(get_keyword().split(','))
