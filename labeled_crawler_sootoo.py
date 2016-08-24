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
class LabeledCrawlerSootoo(LabeledCrawler):
    def __init__(self, proj_name):
        LabeledCrawler.__init__(self, proj_name)
        self.name = "速途网"
        self.root_url = "http://www.sootoo.com"

    def crawl(self, start_time, end_time):
        self.labeled_crawl("http://www.sootoo.com/tag/13/", start_time, end_time, self.cat_dict["电商"])
        self.labeled_crawl("http://www.sootoo.com/tag/204/", start_time, end_time, self.cat_dict["O2O"])
        self.labeled_crawl("http://www.sootoo.com/tag/18/", start_time, end_time, self.cat_dict["游戏&直播"])
        self.labeled_crawl("http://www.sootoo.com/tag/106/", start_time, end_time, self.cat_dict["游戏&直播"])
        self.labeled_crawl("http://health.sootoo.com/", start_time, end_time, self.cat_dict["医疗健康"])
        self.labeled_crawl("http://www.sootoo.com/tag/118/", start_time, end_time, self.cat_dict["物联网"])
        self.labeled_crawl("http://www.sootoo.com/tag/206/", start_time, end_time, self.cat_dict["智能硬件"])
        self.labeled_crawl("http://www.sootoo.com/tag/128/", start_time, end_time, self.cat_dict["企业服务"])
        self.labeled_crawl("http://www.sootoo.com/keyword/85759/", start_time, end_time, self.cat_dict["企业服务"])
        self.labeled_crawl("http://www.sootoo.com/tag/133/", start_time, end_time, self.cat_dict["企业服务"])

    def labeled_crawl(self, start_url, start_time, end_time, a_category):
        try:
            page = 0
            while True:
                page += 1
                html = urllib2.urlopen("%s?page=%d" % (start_url, page)).read()
                soup = BeautifulSoup(html, "lxml")
                div_zxgx = soup.find(name="div", class_="ZXGX")
                if div_zxgx is None:
                    return
                lis = div_zxgx.ul.find_all(name="li", class_="ZXGX_list clearfix")
                for li in lis:
                    if li.img is None:
                        continue
                    img_src = li.img["src"].encode("utf-8")
                    year = re.search( r'.*/msg/(\d+)/(\d+)/(\d+)/.*', img_src).group(1)
                    mdhm = li.p.find_all(name="span")[2].string.strip()[:11].encode("utf-8")
                    a_url = self.root_url + li.h3.a["href"]
                    a_time = year + "-" + mdhm + ":00"
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
            divs = soup.find(name="div", class_="center-research-t").div.find_all(name="div", recursive=False)
            div_txt = divs[0]
            div_foot = divs[1]

            # 标题
            a_title = div_txt.h1.string.encode("utf-8")
            # 作者，时间
            a_author = div_txt.find(name="div", class_="t11_info").div.a.string.encode("utf-8")
            # 正文
            a_text = ""
            plist = div_txt.find(name="div", class_="t11_mlblk t11_contentarea").find_all(name="p")
            for p in plist:
                strings = p.stripped_strings
                for string in strings:
                    a_text = a_text + string.encode('utf-8')
                a_text += "\n"

            # 标签
            a_tags = ""
            alist = div_foot.div.find_all(name="a", recursive=False)
            if alist is not None:
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
    crawler = LabeledCrawlerSootoo(proj_name="article_test")
    crawler.rebuild_table()
    crawler.crawl("2016-01-01 00:00:00", "2016-08-23 23:59:59")
