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
class Crawler163(Crawler):
    def __init__(self):
        Crawler.__init__(self)
        self.name = "网易科技"
        self.root_url = "http://tech.163.com/gd/"

    def crawl(self, start_time, end_time):
        try:
            is_first_page = True
            page = 1
            while True:
                if is_first_page:
                    html = urllib2.urlopen("http://tech.163.com/internet/").read()
                    is_first_page = False
                else:
                    page += 1
                    html = urllib2.urlopen("http://tech.163.com/special/internet_2016_%02d/" % page).read()

                # 获取文章列表
                soup = BeautifulSoup(html, "lxml")
                ul_news_flow_content = soup.find(name="ul", id="news-flow-content")
                lis = ul_news_flow_content.select(" > li")

                # 分析并保存文章
                for li in lis:
                    a_url = li.div.h3.a["href"]  # 文章url
                    a_time = li.find(name="div", class_="newsBottom clearfix").find(name="p", class_="sourceDate").\
                        span.next_sibling.string.encode("utf-8")  # 文章时间
                    if a_time < start_time:  # 如果文章太老了，停止搜索
                        return
                    elif a_time > end_time: # 如果文章太新了，继续搜索，但不保存
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
    @staticmethod
    def parse_html(a_url, a_time):  # 网易正文的时间不好分析，只能从摘要那边截取传入
        # time.sleep(5)
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
        except urllib2.HTTPError, e:
            print "HTTPError:", e.code, e.reason
        except urllib2.URLError, e:
            print "URLError:", e.reason
        except:
            print "未知错误"
        return None

if __name__ == "__main__":
    crawler = Crawler163()
    crawler.rebuild_table()
    crawler.crawl("2016-08-15 00:00:00", "2016-08-19 23:59:59")
