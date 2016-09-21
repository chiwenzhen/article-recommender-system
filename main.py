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
from clustering import LDA
from labeled_crawler import LabeledCrawler
from labeled_crawler_iheima import LabeledCrawlerIheima
from labeled_crawler_kanchai import LabeledCrawlerKanchai
from labeled_crawler_leiphone import LabeledCrawlerLeiphone
from labeled_crawler_lieyun import LabeledCrawlerLieyun
from labeled_crawler_sootoo import LabeledCrawlerSootoo
from labeled_crawler_yiou import LabeledCrawlerYiou
from labeled_crawler_7tin import LabeledCrawler7tin
from labeled_crawler_ailab import LabeledCrawlerAilab
from labeled_crawler_baidu import LabeledCrawlerBaidu
from labeled_crawler_sinavr import LabeledCrawlerSinaVR
from labeled_crawler_varkr import LabeledCrawlerVarkr
from classifier import TextClassifierTfidf
import MySQLdb
from myutils import Article
from myutils import Dumper
from myutils import ArticleDB
import shutil


def fetch_nonlabeled_data():
    proj_name = "article150801160830"
    str_old_time = "2015-08-01 00:00:00"
    str_new_time = "2016-12-31 00:00:00"

    # Crawler(proj_name=proj_name).rebuild_table()
    # Crawler163(proj_name=proj_name).crawl(str_old_time, str_new_time)
    # Crawler36Kr(proj_name=proj_name).crawl(str_old_time, str_new_time)
    # CrawlerGeekPark(proj_name=proj_name).crawl(str_old_time, str_new_time)
    # CrawlerLeiphone(proj_name=proj_name).crawl(str_old_time, str_new_time)
    # CrawlerKanchai(proj_name=proj_name).crawl(str_old_time, str_new_time)
    # CrawlerHuxiu(proj_name=proj_name).crawl(str_old_time, str_new_time)

    LabeledCrawlerIheima(proj_name=proj_name).crawl(str_old_time, str_new_time)
    LabeledCrawlerKanchai(proj_name=proj_name).crawl(str_old_time, str_new_time)
    LabeledCrawlerLeiphone(proj_name=proj_name).crawl(str_old_time, str_new_time)
    LabeledCrawlerLieyun(proj_name=proj_name).crawl(str_old_time, str_new_time)
    LabeledCrawlerSootoo(proj_name=proj_name).crawl(str_old_time, str_new_time)
    LabeledCrawlerYiou(proj_name=proj_name).crawl(str_old_time, str_new_time)
    LabeledCrawler7tin(proj_name=proj_name).crawl("2000-08-01 00:00:00", str_new_time)
    LabeledCrawlerAilab(proj_name=proj_name).crawl("2000-08-01 00:00:00", str_new_time)
    LabeledCrawlerBaidu(proj_name=proj_name).crawl("2000-08-01 00:00:00", str_new_time)
    LabeledCrawlerSinaVR(proj_name=proj_name).crawl("2000-08-01 00:00:00", str_new_time)
    LabeledCrawlerVarkr(proj_name=proj_name).crawl("2000-08-01 00:00:00", str_new_time)

    seg = Segmenter(proj_name=proj_name)
    seg.seg(skip_exist=True)
    seg.join_segfile()


def fetch_labeled_data():
    str_old_time = "2015-08-01 00:00:00"
    str_new_time = "2016-11-31 00:00:00"
    proj_name = "article_cat"

    LabeledCrawler(proj_name=proj_name).rebuild_table()
    LabeledCrawlerIheima(proj_name=proj_name).crawl(str_old_time, str_new_time)
    LabeledCrawlerKanchai(proj_name=proj_name).crawl(str_old_time, str_new_time)
    LabeledCrawlerLeiphone(proj_name=proj_name).crawl(str_old_time, str_new_time)
    LabeledCrawlerLieyun(proj_name=proj_name).crawl(str_old_time, str_new_time)
    LabeledCrawlerSootoo(proj_name=proj_name).crawl(str_old_time, str_new_time)
    LabeledCrawlerYiou(proj_name=proj_name).crawl(str_old_time, str_new_time)
    LabeledCrawler7tin(proj_name=proj_name).crawl("2000-08-01 00:00:00", str_new_time)
    LabeledCrawlerAilab(proj_name=proj_name).crawl("2000-08-01 00:00:00", str_new_time)
    LabeledCrawlerBaidu(proj_name=proj_name).crawl("2000-08-01 00:00:00", str_new_time)
    LabeledCrawlerSinaVR(proj_name=proj_name).crawl("2000-08-01 00:00:00", str_new_time)
    LabeledCrawlerVarkr(proj_name=proj_name).crawl("2000-08-01 00:00:00", str_new_time)

    seg = Segmenter(proj_name=proj_name)
    seg.seg(skip_exist=True)
    seg.join_segfile()


def train_label():
    db = ArticleDB()
    test_proj_name = "article150801160830"
    test_seg_dir = test_proj_name + "/seg/"
    test_obj_dir = test_proj_name + "/clf_tfidf/"
    shutil.rmtree(test_obj_dir, ignore_errors=True)
    os.makedirs(test_obj_dir)
    corpus = []

    # 分类器训练
    print "1. trainning tfidf clf..."
    # clf = TextClassifierTfidf(project_name="article_cat")
    # clf.train()
    # Dumper.save(clf, "tfidf_clf.dat")
    clf = Dumper.load("tfidf_clf.dat")

    # 获取测试语料库文档数量
    results = db.execute("select count(id) from %s" % test_proj_name)
    test_count = results[0][0]

    # 读取测试语料库
    print "2. reading corpus..."
    for i in xrange(1, test_count + 1):
        test_seg_name = test_seg_dir + str(i)
        with open(test_seg_name, "r") as test_seg_file:
            lines = [line.strip() for line in test_seg_file.readlines() if len(line.strip()) > 0]
            doc = " ".join(lines)
            corpus.append(doc)

    # 预测测试语料库category
    print "3. predicting corpus"
    corpus_categories = clf.predict(corpus)

    # 往数据库写入category属性
    print "4. writing corpus prediction to mysql..."
    for i, a_category in enumerate(corpus_categories):
        a_id = i + 1
        sql = "update %s set category=%d where id=%s" % (test_proj_name, a_category, a_id)
        db.execute(sql)
    db.commit()
    db.close()

    # 保存测试语料库到对象二进制文件中
    print "5. generating corpus tfidf vectors..."
    tfidf_vectors = clf.transform(corpus)

    print "6. writing corpus tfidf vectors to disk..."
    for i in xrange(test_count):
        print "%d/%d" % (i+1, test_count)
        obj_name = test_obj_dir + str(i+1)
        Dumper.save(tfidf_vectors[i, :], obj_name)

    print "ok, successfully complete!"

if __name__ == '__main__':
    fetch_nonlabeled_data()
