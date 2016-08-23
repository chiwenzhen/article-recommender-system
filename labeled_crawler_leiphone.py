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
class LabeledCrawlerLeiphone(LabeledCrawler):
    def __init__(self, proj_name):
        LabeledCrawler.__init__(self, proj_name)
        self.name = "猎云网"
        self.root_url = "http://www.lieyunwang.com"
        self.headers = {
            'Host': 'www.leiphone.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Connection': 'keep-alive'
        }

    def crawl(self, start_time, end_time):
        # 注：http://www.leiphone.com/recommend/index/id/54中54换成其他数字，也可以获得大量网页，但是雷锋网上没给出名称
        self.labeled_crawl("http://www.leiphone.com/recommend/index/id/58", start_time, end_time, self.cat_dict["人工智能"])
        self.labeled_crawl("http://www.leiphone.com/recommend/index/id/59", start_time, end_time, self.cat_dict["医疗健康"])
        self.labeled_crawl("http://www.leiphone.com/recommend/index/id/57", start_time, end_time, self.cat_dict["互联网金融"])
        self.labeled_crawl("http://www.leiphone.com/recommend/index/id/55", start_time, end_time, self.cat_dict["汽车"])

    def labeled_crawl(self, start_url, start_time, end_time, a_category):
        try:
            page = 0
            while True:
                page += 1
                url = "%s?page=%d#lph-pageList" % (start_url, page)
                req = urllib2.Request(url, headers=self.headers)
                html = urllib2.urlopen(req).read()
                soup = BeautifulSoup(html, "lxml")
                div_wrap = soup.find(name="div", class_="wrap")
                lis = div_wrap.find_all(name="li", class_="pbox clr")
                for li in lis:
                    div_word = li.find(name="div", class_="word")
                    a_url = div_word.a["href"]
                    spans = div_word.find(name="div", class_="time").find_all("span")
                    str_time = (spans[0].string + u" " + spans[1].string).encode("utf-8")
                    a_time = self.time_normalize(str_time, '%Y / %m / %d %H:%M')
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
            req = urllib2.Request(a_url, headers=self.headers)
            html = urllib2.urlopen(req).read()
            soup = BeautifulSoup(html, "lxml")
            article_left = soup.find(name="div", class_="article-left lph-left")
            # 标题
            a_title = article_left.div.h1.string.encode('utf-8')
            # 作者，时间
            a_author = article_left.find(name="div", class_="pi-author").a.string.encode('utf-8')
            a_time = a_time
            # 正文
            a_text = ""
            plist = article_left.find(name="div", class_="pageCont lph-article-comView ").find_all(name="p")
            for p in plist:
                if p.string is not None:
                    a_text = a_text + p.string.encode('utf-8') + "\n"
            # 标签
            a_tags = ""

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
    crawler = LabeledCrawlerLeiphone(proj_name="article_cat")
    crawler.rebuild_table()
    crawler.crawl("2016-08-16 00:00:00", "2016-08-23 23:59:59")
