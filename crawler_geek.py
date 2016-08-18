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
class GeekparkCrawler(Crawler):
    def __init__(self):
        Crawler.__init__(self, "极客公园", "http://www.geekpark.net")

    def crawl(self, start_time, end_time):
        try:
            # 初次加载的内容
            is_first_page = True
            out_of_date = False
            page = 1
            while True:
                if out_of_date:
                    break
                if is_first_page:
                    html = urllib2.urlopen("http://www.geekpark.net").read()
                else:
                    page += 1
                    html = urllib2.urlopen("http://www.geekpark.net/articles_list?page=%d" % page).read()
                is_first_page = False

                soup = BeautifulSoup(html, "lxml")
                if is_first_page:
                    div_article_item_content = soup.find(name="div", class_="article-item-box article-all active").div
                    article_items = div_article_item_content.find_all(name="article", class_="article-item")
                else:
                    article_items = soup.find_all(name="article", class_="article-item")
                for item in article_items:
                    if out_of_date:
                        break
                    title = item.find(name="a", class_="article-title")
                    href = title["href"]
                    url = self.root_url + href
                    article = self.parse_html(url)
                    if article is None:
                        print "ERROR：GeekPark 网页分析错误！"
                        continue
                    if start_time <= article.a_time <= end_time:  # 如果文章时间刚好，则保存，并继续搜索
                        self.count += 1
                        self.save(article)
                    elif article.a_time > end_time:  # 如果文章太新了，继续搜索，但不保存
                        continue
                    else:  # 如果文章太老了，停止搜索
                        out_of_date = True
        except urllib2.URLError, e:
            print e.reason

    # 分析html, 返回Article对象
    def parse_html(self, a_url):
        time.sleep(5)
        try:
            html = urllib2.urlopen(a_url).read()
            soup = BeautifulSoup(html, "lxml")
            header_top_section = soup.find(name="header", class_="top-section")
            section_main_content = soup.find(name="section", class_="main-content")
            # 标题
            a_title = header_top_section.h1.string.encode('utf-8')
            # 作者，时间
            a_author = header_top_section.div.a.span.string.encode('utf-8')
            a_time = self.time_num2str(float(header_top_section.find(name="span", class_="js-relative-time")["data-time"]))
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
        except urllib2.HTTPError, e:  # HTTPError必须排在URLError的前面
            print "The server couldn't fulfill the request"
            print "Error code:", e.code
            print "Return content:", e.read()
            return None
        except urllib2.URLError, e:
            print "Failed to reach the server"
            print "The reason:", e.reason
            return None

if __name__ == "__main__":
    crawler = GeekparkCrawler()
    crawler.create_table()
    crawler.crawl("2016-08-15 00:00:00", "2016-08-16 23:59:59")
