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
from lda import LDA
from labeled_crawler import LabeledCrawler
from labeled_crawler_iheima import LabeledCrawlerIheima
from labeled_crawler_kanchai import LabeledCrawlerKanchai
from labeled_crawler_leiphone import LabeledCrawlerLeiphone
from labeled_crawler_lieyun import LabeledCrawlerLieyun
from labeled_crawler_sootoo import LabeledCrawlerSootoo
from labeled_crawler_yiou import LabeledCrawlerYiou
from text_classifier import TextClassifier


def fetch_nonlabeled_data():
    proj_name = "article"
    str_old_time = "2015-08-01 00:00:00"
    str_new_time = "2016-08-24 00:00:00"

    Crawler(proj_name=proj_name).rebuild_table()
    Crawler163(proj_name=proj_name).crawl(str_old_time, str_new_time)
    Crawler36Kr(proj_name=proj_name).crawl(str_old_time, str_new_time)
    CrawlerGeekPark(proj_name=proj_name).crawl(str_old_time, str_new_time)
    CrawlerLeiphone(proj_name=proj_name).crawl(str_old_time, str_new_time)
    CrawlerKanchai(proj_name=proj_name).crawl(str_old_time, str_new_time)
    CrawlerHuxiu(proj_name=proj_name).crawl(str_old_time, str_new_time)

    seg = Segmenter(proj_name=proj_name)
    seg.seg()
    seg.join_seg_file()

    LDA(proj_name=proj_name).clustering()


def fetch_labeled_data():
    str_old_time = "2015-08-01 00:00:00"
    str_new_time = "2016-08-25 00:00:00"
    proj_name = "article_cat"

    LabeledCrawler(proj_name=proj_name).rebuild_table()
    LabeledCrawlerIheima(proj_name=proj_name).crawl(str_old_time, str_new_time)
    LabeledCrawlerKanchai(proj_name=proj_name).crawl(str_old_time, str_new_time)
    LabeledCrawlerLeiphone(proj_name=proj_name).crawl(str_old_time, str_new_time)
    LabeledCrawlerLieyun(proj_name=proj_name).crawl(str_old_time, str_new_time)
    LabeledCrawlerSootoo(proj_name=proj_name).crawl(str_old_time, str_new_time)
    LabeledCrawlerYiou(proj_name=proj_name).crawl(str_old_time, str_new_time)

    seg = Segmenter(proj_name=proj_name)
    seg.seg()
    seg.join_seg_file()

    # ArticleLDA(proj_name=proj_name).clustering()
    clf = TextClassifier(project_name="article_cat")
    clf.test()


if __name__ == '__main__':
    fetch_labeled_data()
