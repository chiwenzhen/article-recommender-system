# coding=utf-8
import time
import os
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
from classifier import TextClassifierTfidf
import MySQLdb
from article import Article, ArticleDumper
from articledb import ArticleDB


def fetch_nonlabeled_data():
    proj_name = "article150801160830"
    str_old_time = "2015-08-01 00:00:00"
    str_new_time = "2016-08-31 00:00:00"

    # Crawler(proj_name=proj_name).rebuild_table()
    # Crawler163(proj_name=proj_name).crawl(str_old_time, str_new_time)
    # Crawler36Kr(proj_name=proj_name).crawl(str_old_time, str_new_time)
    # CrawlerGeekPark(proj_name=proj_name).crawl(str_old_time, str_new_time)
    CrawlerLeiphone(proj_name=proj_name).crawl(str_old_time, str_new_time)
    # CrawlerKanchai(proj_name=proj_name).crawl(str_old_time, str_new_time)
    # CrawlerHuxiu(proj_name=proj_name).crawl(str_old_time, str_new_time)

    seg = Segmenter(proj_name=proj_name)
    seg.seg()
    seg.join_seg_file()

    # LDA(proj_name=proj_name).clustering()


def fetch_labeled_data():
    str_old_time = "2015-08-01 00:00:00"
    str_new_time = "2016-08-31 00:00:00"
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


def train_test():
    db = ArticleDB()
    dumper = ArticleDumper()
    test_proj_name = "article15081608"
    test_seg_dir = test_proj_name + "/seg/"
    test_attr_dir = test_proj_name + "/attr/"
    test_obj_dir = test_proj_name + "/obj/"
    corpus = []

    # 分类器训练
    clf = TextClassifierTfidf(project_name="article_cat")
    clf.train()
    print "训练语料库-训练完毕"

    results = db.execute("select count(id) from %s" % test_proj_name)
    test_count = results[0][0]

    # 读取测试语料库
    for i in xrange(1, test_count + 1):
        test_seg_name = test_seg_dir + str(i)
        with open(test_seg_name, "r") as test_seg_file:
            lines = [line.strip() for line in test_seg_file.readlines() if len(line.strip()) > 0]
            doc = " ".join(lines)
            corpus.append(doc)
    print "测试语料库-读取完毕"

    # 预测测试语料库category
    corpus_categories = clf.predict(corpus)
    print "测试语料库-预测完毕"

    # 往数据库写入category属性
    for i, a_category in enumerate(corpus_categories):
        a_id = i + 1
        sql = "update %s set category=%d where id=%s" % (test_proj_name, a_category, a_id)
        db.execute(sql)
    db.commit()
    print "测试语料库-预测结果写入数据库完毕"

    # 保存测试语料库到对象二进制文件中
    doc_vectors = clf.transform(corpus)

    sql = "select id, category from %s order by id" % test_proj_name
    results = db.execute(sql)
    for a_id, a_category in results:
        print a_id
        attr_name = test_attr_dir + str(a_id)
        obj_name = test_obj_dir + str(a_id)
        with open(attr_name, "r") as attr_file:
            lines = attr_file.readlines()
            a_time = lines[0]
            a_title = lines[1]
            a_url = lines[2]
            a_tags = lines[3]
            article = Article(a_title=a_title, a_text=doc_vectors[i, :], a_url=a_url, a_time=a_time, a_tags=a_tags,
                              a_category=a_category)
            dumper.dump(article, obj_name)
    db.close()
    print "测试语料库-预测结果写入数据库完毕"


if __name__ == '__main__':
    fetch_nonlabeled_data()
