# coding=utf-8
import urllib2
import urllib
import time
import json
from lxml import etree
from bs4 import BeautifulSoup
import MySQLdb
import sys
from crawler import Crawler, Article
from labeled_crawler import LabeledCrawler


# 二级分类 for VR
class LabeledCrawler7tin(LabeledCrawler):
    def __init__(self, proj_name):
        LabeledCrawler.__init__(self, proj_name)
        self.name = "青亭网"
        self.root_url = "http://www.7tin.cn"

    def crawl(self, start_time, end_time):
        self.labeled_crawl("http://www.7tin.cn/category/vrjia/page/", 27678, start_time, end_time, self.cat_dict["VR"])

    def labeled_crawl(self, start_url, cid, start_time, end_time, a_category):
        try:
            page = 0
            while True:
                page += 1
                html = urllib2.urlopen("%s%d" % (start_url, page)).read()
                soup = BeautifulSoup(html, "lxml")
                article = soup.find(name="div", class_="newslist xfa-newslist clearfix")
                articles = article.find_all(name="article", recursive=False)
                for article in articles:
                    a_url = article.find(name="header").h2.a["href"]
                    a_time = article.find(name="time").string.encode("utf-8")
                    a_time = self.get_format_time(a_time)
                    a_tag = article.find(name="p", class_="meta").b.text.encode("utf-8").strip()
                    if a_time < start_time:  # 如果文章太老了，停止搜索
                        return
                    elif a_time > end_time:  # 如果文章太新了，继续搜索
                        continue
                    else:  # 如果文章在区间内，则分析文章，并继续搜索
                        # 解析文章html
                        article = self.parse_html(a_url, a_time, a_category, a_tag)
                        if article is None:
                            print "ERROR：文章解析错误！" + a_url
                            continue
                        else:
                            self.count += 1
                            self.save(article)
        except urllib2.HTTPError, e:
            print "HTTPError:", e.code, e.reason
        except urllib2.URLError, e:
            print "URLError:", e.reason
        except:
            print "未知错误"

    # 分析html, 返回Article对象
    def parse_html(self, a_url, a_time, a_category, a_tag):
        try:
            html = urllib2.urlopen(a_url, timeout=30).read()
            soup = BeautifulSoup(html, "lxml")
            div = soup.find(name="div", class_="single-content xfa-contet")
            # 标题
            a_title = div.header.h1.string.encode("utf-8")
            # 作者，时间
            a_author = "暂未分析"
            # 正文
            a_text = ""
            plist = div.article.find_all(name="p", recursive=False)
            for p in plist:
                strings = p.stripped_strings
                for string in strings:
                    a_text = a_text + string.encode('utf-8')
                a_text += "\n"
            # 标签

            article = Article(a_title=a_title, a_text=a_text, a_time=a_time, a_author=a_author, a_url=a_url, a_tags=a_tag, a_category=a_category)
            return article
        except urllib2.HTTPError, e:
            print "HTTPError:", e.code, e.reason
        except urllib2.URLError, e:
            print "URLError:", e.reason
        except:
            print "未知错误"
        return None

    # 返回完整的时间格式
    def get_format_time(self, str_time):
        if "分钟前" in str_time:
            minutes = int(str_time[:str_time.find("分钟前")])
            return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() - minutes * 60.0))
        elif "小时前" in str_time:
            hours = int(str_time[:str_time.find("小时前")])
            return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() - hours * 3600.0))
        elif "-" in str_time:
            return "%s-%s 12:00:00" % (time.strftime('%Y', time.localtime(time.time())), str_time)
        else:
            print "时间格式不明: " + str_time

if __name__ == "__main__":
    crawler = LabeledCrawler7tin(proj_name="article_test")
    crawler.rebuild_table()
    crawler.crawl("2016-08-31 00:00:00", "2016-09-23 23:59:59")
