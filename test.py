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
    tags = u"[\"早期项目\",\"zaoqixiangmu\",1],[\"信息安全\",\"xinxianquan\",2],[\"网络运维\",\"wangluoyunwei\",2]"
    ss = re.findall(u"[\u4e00-\u9fa5]+", tags)
    str_time = "http://upload.ikanchai.com/2016/0822/thumb_250_165_1471856056371.jpg"
    str_time = str_time[-17:-2]

    print str_time