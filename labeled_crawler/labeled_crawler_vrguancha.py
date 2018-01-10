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
class LabeledCrawlerVrguancha(LabeledCrawler):
    def __init__(self, proj_name):
        LabeledCrawler.__init__(self, proj_name)
        self.name = "VR观察室"
        self.root_url = "http://www.vrguancha.net"

    def crawl(self, start_time, end_time):
        self.labeled_crawl("http://www.vrguancha.net/plus/list.php?tid=40&PageNo=", start_time, end_time, self.cat_dict["人工智能"], "VR+媒体")
        self.labeled_crawl("http://www.vrguancha.net/plus/list.php?tid=44&PageNo=", start_time, end_time, self.cat_dict["人工智能"], "VR+购物")
        self.labeled_crawl("http://www.vrguancha.net/plus/list.php?tid=48&PageNo=", start_time, end_time, self.cat_dict["人工智能"], "VR+房产")
        self.labeled_crawl("http://www.vrguancha.net/plus/list.php?tid=41&PageNo=", start_time, end_time, self.cat_dict["人工智能"], "VR+旅游")
        self.labeled_crawl("http://www.vrguancha.net/plus/list.php?tid=49&PageNo=", start_time, end_time, self.cat_dict["人工智能"], "VR+游戏")
        self.labeled_crawl("http://www.vrguancha.net/plus/list.php?tid=46&PageNo=", start_time, end_time, self.cat_dict["人工智能"], "VR+影视")
        self.labeled_crawl("http://www.vrguancha.net/plus/list.php?tid=47&PageNo=", start_time, end_time, self.cat_dict["人工智能"], "VR+教育")
        self.labeled_crawl("http://www.vrguancha.net/plus/list.php?tid=50&PageNo=", start_time, end_time, self.cat_dict["人工智能"], "VR+汽车")

    def labeled_crawl(self, start_url, start_time, end_time, a_category, subcategory):
        try:
            page = 0
            while True:
                page += 1
                html = urllib2.urlopen("%s%d" % (start_url, page)).read()
                soup = BeautifulSoup(html, "lxml")
                divs = soup.find(name="div", class_="hlgd-content").find_all(name="div", class_="hlgd-box")
                if len(divs) == 0:
                    return
                for div in divs:
                    a_url = self.root_url + div.dl.dd.h3.a["href"]
                    a_time = div.dl.dd.find_all(name="p")[1].string.encode("utf-8")[-10:]
                    if a_time < start_time:  # 如果文章太老了，停止搜索
                        return
                    elif a_time > end_time:  # 如果文章太新了，继续搜索
                        continue
                    else:  # 如果文章在区间内，则分析文章，并继续搜索
                        # 解析文章html
                        article = self.parse_html(a_url, a_time, a_category, subcategory)
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
    def parse_html(self, a_url, a_time, a_category, subcategory):
        try:
            html = urllib2.urlopen(a_url, timeout=30).read()
            soup = BeautifulSoup(html, "lxml")
            div = soup.find(name="div", class_="hl_content")
            # 标题
            a_title = div.find(name="div", class_="hl_c_title").h2.string.encode("utf-8")
            # 作者，时间
            a_author = div.find(name="div", class_="hl_c_twid").span.string[3:].encode("utf-8")
            # 正文
            a_text = ""
            plist = div.find(name="div", class_="hl_body").find_all(name="p")
            for p in plist:
                strings = p.stripped_strings
                for string in strings:
                    a_text = a_text + string.encode('utf-8')
                a_text += "\n"
            # 标签
            a_tags = subcategory

            article = Article(a_title=a_title, a_text=a_text, a_time=a_time, a_author=a_author, a_url=a_url,
                              a_tags=a_tags, a_category=a_category)
            return article
        except urllib2.HTTPError, e:
            print "HTTPError:", e.code, e.reason
        except urllib2.URLError, e:
            print "URLError:", e.reason
        except:
            print "未知错误"
        return None

if __name__ == "__main__":
    crawler = LabeledCrawlerVrguancha(proj_name="article_cat")
    # crawler.rebuild_table()
    crawler.crawl("2010-08-10 00:00:00", "2016-10-23 23:59:59")
