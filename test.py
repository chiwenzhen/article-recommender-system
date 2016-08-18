# !/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib
import urllib2
import time
import os
import re

def main():
    string = ' '
    print len(string)
    string = string.str
    print len(string)
    return 0

if __name__ == '__main__':
    m = re.match(r'<script>var props=.*\\}\\}\\]\\},locationnal', "<script>var props=77777777333423423dsfdsf\}\}\]\},locationnal")
    if m:
        print "1: ", m.group()

    m = re.match(r'<script>var props=', "<script>var props=77777777333423423dsfdsf\}\}\]\},locationnal")
    if m:
        print "2: ", m.group()

