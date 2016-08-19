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


# 虎嗅爬虫
class CrawlerGeekPark(Crawler):
    def __init__(self):
        Crawler.__init__(self)
        self.name = "极客公园"
        self.root_url = "http://www.geekpark.net"

    def crawl(self, start_time, end_time):
        try:
            # 初次加载的内容
            is_first_page = True
            out_of_date = False
            page = 1
            while True:
                if is_first_page:
                    is_first_page = False
                    html = urllib2.urlopen("http://www.geekpark.net").read()
                else:
                    page += 1
                    html = urllib2.urlopen("http://www.geekpark.net/articles_list?page=%d" % page).read()

                soup = BeautifulSoup(html, "lxml")
                if is_first_page:
                    div_article_item_content = soup.find(name="div", class_="article-item-box article-all active").div
                    article_items = div_article_item_content.find_all(name="article", class_="article-item")
                else:
                    article_items = soup.find_all(name="article", class_="article-item")

                for item in article_items:
                    title = item.find(name="a", class_="article-title")
                    href = title["href"]
                    a_url = self.root_url + href
                    title = item.find(name="a", class_="article-time js-relative-time dib-middle")
                    a_time = title["title"]
                    if a_time < start_time:  # 如果文章太老了，停止搜索
                        return
                    elif a_time > end_time: # 如果文章太新了，继续搜索
                        continue
                    else:  # 如果文章在区间内，则分析文章，并继续搜索
                        # 解析文章html
                        article = self.parse_html(a_url, a_time)
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
    def parse_html(self, a_url, a_time):
        # time.sleep(5)
        try:
            html = urllib2.urlopen(a_url).read()
            soup = BeautifulSoup(html, "lxml")
            header_top_section = soup.find(name="header", class_="top-section")
            section_main_content = soup.find(name="section", class_="main-content")
            # 标题
            a_title = header_top_section.h1.string.encode('utf-8')
            # 作者，时间
            a_author = header_top_section.div.a.span.string.encode('utf-8')
            a_time = a_time
            # 正文
            a_text = ""
            plist = section_main_content.find(name="div", class_="article-content").find_all(name="p")
            for p in plist:
                if p.string is not None:
                    a_text = a_text + p.string.encode('utf-8') + "\n"
            # 标签
            a_tags = ""
            section_tags = section_main_content.section
            if section_tags is not None:
                alist = section_tags.find_all(name="a")
            else:
                alist = []
            for a in alist:
                if a.string is not None:
                    a_tags = a_tags + a.string.encode('utf-8') + " "

            article = Article(a_title=a_title, a_text=a_text, a_time=a_time, a_author=a_author, a_url=a_url, a_tags=a_tags)
            return article
        except urllib2.HTTPError, e:
            print "HTTPError:", e.code, e.reason
        except urllib2.URLError, e:
            print "URLError:", e.reason
        except:
            print "未知错误"
        return None

if __name__ == "__main__":
    crawler = CrawlerGeekPark()
    crawler.delete_all_data()
    crawler.crawl("2016-08-15 00:00:00", "2016-08-16 23:59:59")
