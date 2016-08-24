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
    seg_file = open("a.txt", "r")
    lines = seg_file.readlines()
    print "total %d lines" % len(lines)
    for line in lines:
        print line
