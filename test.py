# !/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import time
import urllib
import urllib2
from collections import defaultdict

def main():
    try:
        i = 0
        i += 10
        raise Exception('spam', 'eggs')
        return 0
    except Exception as inst:
        print "catch exception", inst
        return -1
    finally:
        print "finally"
    return -2

if __name__ == '__main__':
    groups = re.search(r'.*/msg/(\d+)/(\d+)/(\d+)/.*', "http://p.sootoo.com/son_media/msg/2016/06/24/732223.jpg")
    year = groups.group(1)
    print year
