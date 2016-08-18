# coding=utf-8
from crawler_36kr import Kr36Crawler
from crawler_163 import NeteaseCrawler
from crawler_geek import GeekparkCrawler
from crawler_huxiu import HuxiuCrawler
from word_segment import Segmenter


if __name__ == '__main__':
    crawlers = [NeteaseCrawler(), Kr36Crawler(), GeekparkCrawler(), HuxiuCrawler()]

    for crawler in crawlers:
        crawler.crawl("2016-07-18 00:00:00", "2016-08-18 23:59:59")

    seg = Segmenter()
    seg.seg()
