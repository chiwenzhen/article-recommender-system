# coding=utf-8
import time
from crawler_36kr import Crawler36Kr
from crawler_163 import Crawler163
from crawler_geek import CrawlerGeekPark
from crawler_huxiu import CrawlerHuxiu
from crawler import Crawler
from crawler_leiphone import CrawlerLeiphone
from crawler_kanchai import CrawlerKanchai
from segmenter import Segmenter
from clustering import ArticleClustering


if __name__ == '__main__':

    Crawler(table="article", save_dir="articles").rebuild_table()

    str_old_time = "2015-08-01 00:00:00"
    str_new_time = "2016-08-24 00:00:00"
    Crawler163().crawl(str_old_time, str_new_time)
    Crawler36Kr().crawl(str_old_time, str_new_time)
    CrawlerGeekPark().crawl(str_old_time, str_new_time)
    CrawlerLeiphone().crawl(str_old_time, str_new_time)
    CrawlerKanchai().crawl(str_old_time, str_new_time)
    CrawlerHuxiu().crawl(str_old_time, str_new_time)

    seg = Segmenter()
    seg.seg()

    ArticleClustering("articles").clustering()
