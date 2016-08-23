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


# 虎嗅爬虫
class LabeledCrawlerKanchai(LabeledCrawler):
    def __init__(self, proj_name):
        LabeledCrawler.__init__(self, proj_name)
        self.name = "砍柴网"
        self.root_url = "http://www.ikanchai.com"

    def crawl(self, start_time, end_time):
        # 注：http://www.leiphone.com/recommend/index/id/54中54换成其他数字，也可以获得大量网页，但是雷锋网上没给出名称
        self.labeled_crawl("http://news.ikanchai.com/mobile/", start_time, end_time, self.cat_dict["手机"])
        self.labeled_crawl("http://news.ikanchai.com/jiadian/", start_time, end_time, self.cat_dict["智能硬件"])
        self.labeled_crawl("http://news.ikanchai.com/shouyou/", start_time, end_time, self.cat_dict["游戏&直播"])
        self.labeled_crawl("http://www.ikanchai.com/vr/", start_time, end_time, self.cat_dict["VR"])
        self.labeled_crawl("http://www.ikanchai.com/start/", start_time, end_time, self.cat_dict["资本"])
        self.labeled_crawl_pingce("http://www.ikanchai.com/evaluation/", start_time, end_time, self.cat_dict["评测"])

    def labeled_crawl(self, start_url, start_time, end_time, a_category):
        try:
            page = 0
            while True:
                page += 1
                html = urllib2.urlopen("%s%d.shtml" % (start_url, page)).read()
                soup = BeautifulSoup(html, "lxml")
                div_content = soup.find(name="div", class_="hlgd-content")
                divs = div_content.find_all(name="div", class_="hlgd-box")
                for div in divs:
                    a_url = div.dl.dd.h3.a["href"]
                    a_time = div.dl.dd.find_all(name="p")[1].string[-16:].encode("utf-8")
                    if a_time < start_time:  # 如果文章太老了，停止搜索
                        return
                    elif a_time > end_time:  # 如果文章太新了，继续搜索
                        continue
                    else:  # 如果文章在区间内，则分析文章，并继续搜索
                        # 解析文章html
                        article = self.parse_html(a_url, a_time, a_category)
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


    def labeled_crawl_pingce(self, start_url, start_time, end_time, a_category):
        try:
            page = 0
            while True:
                page += 1
                html = urllib2.urlopen("%s%d.shtml" % (start_url, page)).read()
                soup = BeautifulSoup(html, "lxml")
                div_znyj_c = soup.find(name="div", class_="znyj_c")
                divs = div_znyj_c.find_all(name="div", class_="znyj_c_box")
                for div in divs:
                    li = div.ul.find_all(name="li", recursive=False)[1]
                    a_url = li.dl.dt.a["href"]
                    a_time = li.dl.dd.p.string[-16:].encode("utf-8")
                    if a_time < start_time:  # 如果文章太老了，停止搜索
                        return
                    elif a_time > end_time:  # 如果文章太新了，继续搜索
                        continue
                    else:  # 如果文章在区间内，则分析文章，并继续搜索
                        # 解析文章html
                        article = self.parse_html(a_url, a_time, a_category)
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
    def parse_html(self, a_url, a_time, a_category):
        try:
            html = urllib2.urlopen(a_url).read()
            soup = BeautifulSoup(html, "lxml")
            div_hl_content = soup.find(name="div", class_="hl_content")
            # 标题
            a_title = div_hl_content.find(name="div", class_="hl_c_title").h2.contents[0].encode("utf-8")
            # 作者，时间
            a_author = "暂未提取"
            # 正文
            a_text = ""
            plist = div_hl_content.find(name="div", class_="hl_body").find_all(name="p")
            for p in plist:
                if p.string is not None:
                    a_text = a_text + p.string.encode('utf-8') + "\n"
            # 标签
            a_tags = ""
            div_hl_c_tagl = div_hl_content.find(name="div", class_="hl_c_tagl")

            if div_hl_c_tagl is not None:
                lis = div_hl_c_tagl.ul.find_all(name="li")
            else:
                alist = []
            if len(lis) > 0:
                alist = [li.a.string.encode('utf-8') for li in lis]
                a_tags = " ".join(alist)

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
    crawler = LabeledCrawlerKanchai(proj_name="article_cat")
    crawler.rebuild_table()
    crawler.crawl("2016-08-10 00:00:00", "2016-08-23 23:59:59")
