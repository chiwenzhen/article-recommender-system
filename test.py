# !/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib
import urllib2
import time
import os
import re

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

    print m.group()
