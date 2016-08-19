# coding=utf-8
import time
from crawler_36kr import Crawler36Kr
from crawler_163 import Crawler163
from crawler_geek import CrawlerGeekPark
from crawler_huxiu import CrawlerHuxiu
from crawler import Crawler
from crawler_leiphone import CrawlerLeiphone
from word_segment import Segmenter


if __name__ == '__main__':

    # Crawler().delete_all_data()
    #
    # str_old_time = "2016-08-01 00:00:00"
    # str_new_time = "2016-08-20 00:00:00"
    # Crawler163().crawl(str_old_time, str_new_time)
    # Crawler36Kr().crawl(str_old_time, str_new_time)
    # CrawlerGeekPark().crawl(str_old_time, str_new_time)
    # CrawlerLeiphone().crawl(str_old_time, str_new_time)
    # CrawlerHuxiu().crawl(str_old_time, str_new_time)

    seg = Segmenter()
    seg.seg()
