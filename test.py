# !/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib
import urllib2


def main():
    url = "http://www.douban.com"
    # 浏览器头
    # headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    req = urllib2.Request(url=url)
    data = urllib2.urlopen(req).read()
    print data
    return 0


if __name__ == '__main__':
    main()
