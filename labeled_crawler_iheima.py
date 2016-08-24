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
import re


# 虎嗅爬虫
class LabeledCrawlerIheima(LabeledCrawler):
    def __init__(self, proj_name):
        LabeledCrawler.__init__(self, proj_name)
        self.name = "i黑马"
        self.root_url = "http://www.iheima.com/"
        self.headers = {
            'Host': 'www.iheima.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Connection': 'keep-alive',
            'X-Requested-With': 'XMLHttpRequest',
        }

    def crawl(self, start_time, end_time):
        self.labeled_crawl("http://www.iheima.com/scope/49", start_time, end_time, self.cat_dict["企业服务"])
        self.labeled_crawl("http://www.iheima.com/scope/46", start_time, end_time, self.cat_dict["VR"])
        self.labeled_crawl("http://www.iheima.com/scope/48", start_time, end_time, self.cat_dict["文创"])
        self.labeled_crawl("http://www.iheima.com/scope/53", start_time, end_time, self.cat_dict["游戏&直播"])
        self.labeled_crawl("http://www.iheima.com/scope/57", start_time, end_time, self.cat_dict["资本"])
        self.labeled_crawl("http://www.iheima.com/scope/60", start_time, end_time, self.cat_dict["智能硬件"])
        self.labeled_crawl("http://www.iheima.com/scope/84", start_time, end_time, self.cat_dict["资本"])
        self.labeled_crawl("http://www.iheima.com/scope/83", start_time, end_time, self.cat_dict["房产"])
        self.labeled_crawl("http://www.iheima.com/scope/58", start_time, end_time, self.cat_dict["农业"])
        self.labeled_crawl("http://www.iheima.com/scope/56", start_time, end_time, self.cat_dict["医疗健康"])
        self.labeled_crawl("http://www.iheima.com/scope/55", start_time, end_time, self.cat_dict["互联网金融"])
        self.labeled_crawl("http://www.iheima.com/scope/54", start_time, end_time, self.cat_dict["教育"])
        self.labeled_crawl("http://www.iheima.com/scope/52", start_time, end_time, self.cat_dict["汽车"])
        self.labeled_crawl("http://www.iheima.com/scope/51", start_time, end_time, self.cat_dict["O2O"])
        self.labeled_crawl("http://www.iheima.com/scope/50", start_time, end_time, self.cat_dict["电商"])
        self.labeled_crawl("http://www.iheima.com/scope/85", start_time, end_time, self.cat_dict["旅游"])

    def labeled_crawl(self, start_url, start_time, end_time, a_category):
        try:
            # 初次加载的内容
            is_first_page = True
            sid = None
            page = 1
            while True:
                if is_first_page:
                    is_first_page = False
                    html = urllib2.urlopen(start_url).read()
                    soup = BeautifulSoup(html, "lxml")
                    div = soup.find(name="div", class_="listitem cf")
                    articles = div.find_all(name="article", class_="item-wrap cf")
                    href = soup.find(name="a", class_="more")["href"]
                    sid = re.search(r".*sid=(\d+)", href).group(1)
                else:
                    page += 1
                    url = start_url + "?page=" + str(page) + "&category=%E5%85%A8%E9%83%A8&sid=" + sid
                    req = urllib2.Request(url, headers=self.headers)
                    html = urllib2.urlopen(req).read()
                    soup = BeautifulSoup(html, "lxml")
                    articles = soup.find_all(name="article", class_="item-wrap cf")
                    if len(articles) == 0:
                        return

                for article in articles:
                    a_url = article.div.div.a["href"]
                    a_time = article.find(name="span", class_="timeago").string.strip().encode("utf-8")
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
            div = soup.find(name="div", class_="main-content")
            # 标题
            a_title = div.div.string.encode('utf-8')
            # 作者，时间
            a_author = div.find(name="div", class_="author").find(name="span", class_="name").string.encode('utf-8')
            # 正文
            a_text = ""
            div_var = div.find(name="div", class_="left523")
            if div_var is not None:
                plist = div_var.find_all(name="p", recursive=False)
            else:
                plist = div.find_all(name="p", recursive=False)
            for p in plist:
                strings = p.stripped_strings
                for string in strings:
                    a_text = a_text + string.encode('utf-8')
                a_text += "\n"
            # 标签
            a_tags = ""
            div_tags = div.find(name="div", class_="fl tags")
            if div_tags is not None:
                alist = div_tags.find_all(name="span")
            else:
                alist = []
            if len(alist) > 0:
                alist = [a.string.encode('utf-8') for a in alist]
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
    crawler = LabeledCrawlerIheima(proj_name="article_test")
    crawler.rebuild_table()
    crawler.crawl("2016-08-15 00:00:00", "2016-08-23 23:59:59")
