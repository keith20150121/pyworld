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

if __name__ == '__main__':
    print('gotceleb do nothing as main')

def current():
    return sys.path[0] + '/'

def get_keyword(keyword):
    f = open(current() + keyword, 'r')
    keywords = f.read()
    print(keywords)
    f.close()
    return keywords

class Fetch:
    def __init__(self):
        keywords = get_keyword(current() + 'keyword-list.txt')
        keywords = keywords.split(',')
        
        
        
