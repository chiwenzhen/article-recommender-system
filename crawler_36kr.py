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
import re


# 虎嗅爬虫
class Kr36Crawler(Crawler):
    def __init__(self):
        Crawler.__init__(self, "36氪", "http://36kr.com")

    def crawl(self, start_time, end_time):
        try:
            out_of_date = False
            # 初次加载的内容
            html = urllib2.urlopen("http://36kr.com").read()
            soup = BeautifulSoup(html, "lxml")
            scriptstr = soup.find(name="script", text=re.compile("var props")).string.encode("utf-8")
            scriptstr = scriptstr[10:scriptstr.find(",locationnal")]
            json_obj = json.loads(scriptstr)
            items = json_obj["feedPostsLatest|post"]
            for item in items:
                if out_of_date:
                    break
                article_id = item["id"].encode("utf-8")
                url = (self.root_url + "/p/" + article_id + ".html").encode("utf-8")
                a_time = item["published_at"].encode("utf-8")
                article = self.parse_html(url, a_time)
                if article is None:
                    print "ERROR：36氪 网页分析错误！"
                    continue
                if start_time <= article.a_time <= end_time:  # 如果文章时间刚好，则保存，并继续搜索
                    self.count += 1
                    self.save(article)
                elif article.a_time > end_time:  # 如果文章太新了，继续搜索，但不保存
                    continue
                else:  # 如果文章太老了，停止搜索
                    out_of_date = True
            last_id = items[-1]["id"]

            page = 1
            while True:
                if out_of_date:
                    break

                html = urllib2.urlopen("http://36kr.com/api/info-flow/main_site/posts?column_id=&b_id=%s&per_page=20&_=1471506396638" % last_id).read()
                json_obj = json.loads(html)
                data = json_obj["data"]
                page += 1
                total_pages = data["total_pages"]
                if page >= total_pages:
                    break
                items = data["items"]
                for item in items:
                    if out_of_date:
                        break
                    article_id = item["id"]
                    url = (self.root_url + "/p/" + str(article_id) + ".html").encode("utf-8")
                    a_time = item["published_at"].encode("utf-8")
                    article = self.parse_html(url, a_time)
                    if article is None:
                        print "ERROR：36氪 网页分析错误！"
                        continue
                    if start_time <= article.a_time <= end_time:  # 如果文章时间刚好，则保存，并继续搜索
                        self.count += 1
                        self.save(article)
                    elif article.a_time > end_time:  # 如果文章太新了，继续搜索，但不保存
                        continue
                    else:  # 如果文章太老了，停止搜索
                        out_of_date = True
                last_id = items[-1]["id"]
        except urllib2.URLError, e:
            print e.reason

    # 分析html, 返回Article对象
    def parse_html(self, a_url, a_time):
        time.sleep(5)
        try:
            html = urllib2.urlopen(a_url).read()
            soup = BeautifulSoup(html, "lxml")
            scriptstr = soup.find(name="script", text=re.compile("var props")).string.encode("utf-8")
            scriptstr = scriptstr[10:scriptstr.find(",locationnal")]
            json_obj = json.loads(scriptstr)
            data = json_obj["detailArticle|post"]
            # 标题
            a_title = data["title"].encode('utf-8')
            # 作者，时间
            a_author = data["user"]["name"].encode('utf-8')
            a_time = a_time
            # 正文
            a_text = ""
            soup = BeautifulSoup(data["content"], "lxml")
            plist = soup.find_all(name="p")
            for p in plist:
                if p.string is not None:
                    a_text = a_text + p.string.encode('utf-8') + "\n"
            # 标签
            a_tags = ""
            tags = data["extraction_tags"]  #"extraction_tags": "[[\"早期项目\",\"zaoqixiangmu\",1],[\"信息安全\",\"xinxianquan\",2],[\"网络运维\",\"wangluoyunwei\",2]]"
            if tags is not None:
                    str_tag = re.match(ur"[\u4e00-\u9fa5]+", tags)
                    if str_tag is not None:  # 这里正则表达匹配失败，不知为何？？
                        a_tags += str_tag

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
    crawler = Kr36Crawler()
    crawler.create_table()
    crawler.crawl("2016-08-15 00:00:00", "2016-08-19 23:59:59")
