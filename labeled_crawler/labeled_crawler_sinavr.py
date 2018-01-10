# coding=utf-8
import urllib2
import urllib
import time
import json
from lxml import etree
from bs4 import BeautifulSoup, NavigableString
import MySQLdb
import sys
from crawler import Crawler, Article
from labeled_crawler import LabeledCrawler


# 二级分类 for VR
class LabeledCrawlerSinaVR(LabeledCrawler):
    def __init__(self, proj_name):
        LabeledCrawler.__init__(self, proj_name)
        self.name = "新浪VR"
        self.root_url = "http://vr.sina.cn"

    def crawl(self, start_time, end_time):
        self.labeled_crawl("http://vr.sina.cn/pc/newslist.shtml?k=5&page=", start_time, end_time, self.cat_dict["VR"], "硬件前沿")
        self.labeled_crawl("http://vr.sina.cn/pc/newslist.shtml?k=6&page=", start_time, end_time, self.cat_dict["VR"], "技术速递")
        self.labeled_crawl("http://vr.sina.cn/pc/newslist.shtml?k=4&page=", start_time, end_time, self.cat_dict["VR"], "游戏咨询")
        self.labeled_crawl("http://vr.sina.cn/pc/newslist.shtml?k=18&page=", start_time, end_time, self.cat_dict["VR"], "游戏评测")
        self.labeled_crawl("http://vr.sina.cn/pc/newslist.shtml?k=2&page=", start_time, end_time, self.cat_dict["VR"], "行业动态")

    def labeled_crawl(self, start_url, start_time, end_time, a_category, a_tag):
        try:
            page = 0
            while True:
                page += 1
                html = urllib2.urlopen("%s%d" % (start_url, page)).read()
                soup = BeautifulSoup(html, "lxml")
                div_list = soup.find(name="div", class_="news-list-detail")
                if div_list is None:
                    return

                divs = div_list.find_all(name="div", class_="listboxwp", recursive=False)
                for div in divs:
                    a_url = div.h3.a["href"]
                    for content in div.contents:
                        if isinstance(content, NavigableString):
                            a_time = content.string.encode("utf-8").strip()
                            break
                    a_time = a_time + " " + div.find(name="span", class_="time").string.encode("utf-8")
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
            div = soup.find(name="div", class_="crticalcontent")
            # 标题
            a_title = div.span.h1.string.encode("utf-8")
            # 作者，时间
            a_author = "暂未分析"
            # 正文
            a_text = ""
            plist = div.find(name="div", id="artibody").find_all(name="p", recursive=False)
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
    crawler = LabeledCrawlerSinaVR(proj_name="article_test")
    crawler.rebuild_table()
    crawler.crawl("2016-08-31 00:00:00", "2016-09-23 23:59:59")
