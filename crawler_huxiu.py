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
class CrawlerHuxiu(Crawler):
    def __init__(self):
        Crawler.__init__(self)
        self.name = "虎嗅"
        self.root_url = "http://www.huxiu.com"

    def crawl(self, start_time, end_time):
        try:
            # 初次加载的内容
            html = urllib2.urlopen("https://www.huxiu.com/startups.html").read()
            soup = BeautifulSoup(html, "lxml")
            divs = soup.select("div .mod-b.mod-art")
            for div in divs:
                href = div.div.a["href"]
                url = self.root_url + href
                article = self.parse_html(url)
                if article is None:
                    print "ERROR：虎嗅 网页分析错误！"
                    continue
                if start_time <= article.a_time <= end_time:  # 如果文章时间刚好，则保存，并继续搜索
                    self.count += 1
                    self.save(article)
                elif article.a_time > end_time:  # 如果文章太新了，继续搜索，但不保存
                    continue
                else:  # 如果文章太老了，停止搜索
                    return

            # 点击加载更多
            last_dateline = \
            soup.find(lambda e: e.name == "div" and e.has_attr("data-cur_page") and e.has_attr("data-catid"))[
                "data-last_dateline"]
            params = {'huxiu_hash_code': "dc93f40d0f51b128d6c60db186fd5c89", 'page': 1, 'catid': 2,
                      "last_dateline": last_dateline}
            req_url = 'https://www.huxiu.com/v2_action/article_list'
            while True:
                params["page"] += 1
                params["last_dateline"] = last_dateline
                req_form = urllib.urlencode(params)
                request = urllib2.Request(url=req_url, data=req_form)
                response = urllib2.urlopen(request).read()
                json_obj = json.loads(response)
                total_page = json_obj["total_page"]
                if params["page"] >= total_page:  # 超过最多加载页数
                    return
                last_dateline = json_obj["last_dateline"]
                soup = BeautifulSoup(json_obj['data'], "lxml")
                divs = soup.find_all(name="div", class_="mod-b mod-art")
                for div in divs:
                    href = div.div.a["href"]
                    url = self.root_url + href
                    article = self.parse_html(url)
                    if article is None:
                        print "ERROR：虎嗅 网页分析错误！"
                        continue
                    if start_time <= article.a_time <= end_time:  # 如果文章时间刚好，则保存，并继续搜索
                        self.count += 1
                        self.save(article)
                    elif article.a_time > end_time:  # 如果文章太新了，继续搜索，但不保存
                        continue
                    else:  # 如果文章太老了，停止搜索
                        return
        except urllib2.HTTPError, e:
            print "HTTPError:", e.code, e.reason
        except urllib2.URLError, e:
            print "URLError:", e.reason
        except:
            print "未知错误"

    # 分析html, 返回Article对象
    @staticmethod
    def parse_html(a_url):
        # time.sleep(5)
        try:
            html = urllib2.urlopen(a_url).read()

            soup = BeautifulSoup(html, "lxml")
            article_wrap = soup.find(name="div", class_="article-wrap")
            # 标题
            a_title = article_wrap.h1.string.encode('utf-8')
            # 作者，时间
            article_author = article_wrap.find(name="div", class_="article-author")
            a_author = article_author.span.a.string.encode('utf-8')
            a_time = article_author.find(name="span", class_="article-time").string.encode('utf-8')
            # 正文
            a_text = ""
            plist = article_wrap.find(name="div", class_="article-content-wrap").find_all(name="p")
            for p in plist:
                if p.string is not None:
                    a_text = a_text + p.string.encode('utf-8') + "\n"
            # 标签
            a_tags = ""
            div_tag_box = article_wrap.find(name="div", class_="tag-box ")
            if div_tag_box is not None:
                alist = div_tag_box.ul.find_all(name="a")
            else:
                alist = []

            for a in alist:
                if a.li.string is not None:
                    a_tags = a_tags + a.li.string.encode('utf-8') + " "

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
    crawler = CrawlerHuxiu()
    crawler.delete_all_data()
    crawler.crawl("2016-08-15 00:00:00", "2016-08-19 23:59:59")
