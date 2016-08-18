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
class NeteaseCrawler(Crawler):
    def __init__(self):
        Crawler.__init__(self, "网易科技", "http://tech.163.com/gd/")

    def crawl(self, start_time, end_time):
        try:
            is_first_page = True
            out_of_date = False
            page = 1
            while True:
                if out_of_date:
                    break
                if is_first_page:
                    html = urllib2.urlopen("http://tech.163.com/internet/").read()
                else:
                    page += 1
                    html = urllib2.urlopen("http://tech.163.com/special/internet_2016_%02d/" % page).read()
                is_first_page = False

                soup = BeautifulSoup(html, "lxml")
                ul_news_flow_content = soup.find(name="ul", id="news-flow-content")
                lis = ul_news_flow_content.select(" > li")
                for li in lis:
                    if out_of_date:
                        break
                    url = li.div.h3.a["href"]
                    a_time = li.find(name="div", class_="newsBottom clearfix").find(name="p", class_="sourceDate").span.next_sibling.string.encode("utf-8")
                    article = self.parse_html(url, a_time)
                    if article is None:
                        print "ERROR：163 网页分析错误！"
                        continue
                    if start_time <= article.a_time <= end_time:  # 如果文章时间刚好，则保存，并继续搜索
                        self.count += 1
                        self.save(article)
                    elif article.a_time > end_time: # 如果文章太新了，继续搜索，但不保存
                        continue
                    else:  # 如果文章太老了，停止搜索
                        out_of_date = True
        except urllib2.URLError, e:
            print e.reason

    # 分析html, 返回Article对象
    @staticmethod
    def parse_html(a_url, a_time):  # 网易正文的时间不好分析，只能从摘要那边截取传入
        time.sleep(5)
        try:
            html = urllib2.urlopen(a_url).read()
            soup = BeautifulSoup(html, "lxml")

            div_post_content_main = soup.find(name="div", class_="post_content_main")
            # 标题
            a_title = div_post_content_main.h1.string.encode('utf-8')
            # 作者，时间
            a_author = div_post_content_main.div.a.string.encode('utf-8')
            a_time = a_time
            # 正文
            a_text = ""
            plist = div_post_content_main.find(name="div", class_="post_text").find_all("p")
            for p in plist:
                if p.string is not None:
                    a_text = a_text + p.string.encode('utf-8') + "\n"
            # 标签
            a_tags = ""
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
    crawler = NeteaseCrawler()
    crawler.create_table()
    crawler.crawl("2016-08-15 00:00:00", "2016-08-18 23:59:59")
