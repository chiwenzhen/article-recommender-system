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
class Crawler36Kr(Crawler):
    def __init__(self, proj_name):
        Crawler.__init__(self, proj_name)
        self.name = "36氪"
        self.root_url = "http://36kr.com"

    def crawl(self, start_time, end_time):
        try:
            is_first_page = True
            page = 1
            last_id = None
            while True:
                if is_first_page:
                    is_first_page = False
                    html = urllib2.urlopen("http://36kr.com").read()
                    soup = BeautifulSoup(html, "lxml")
                    scriptstr = soup.find(name="script", text=re.compile("var props")).string.encode("utf-8")
                    scriptstr = scriptstr[10:scriptstr.find(",locationnal")]
                    json_obj = json.loads(scriptstr)
                    items = json_obj["feedPostsLatest|post"]
                else:
                    html = urllib2.urlopen(
                        "http://36kr.com/api/info-flow/main_site/posts?column_id=&b_id=%s&per_page=20&_=1471506396638" % last_id).read()
                    json_obj = json.loads(html)
                    data = json_obj["data"]
                    page += 1
                    total_pages = data["total_pages"]
                    if page >= total_pages:
                        print "36氪已经没有更多数据了..."
                        return
                    items = data["items"]

                for item in items:
                    article_id = item["id"]
                    if isinstance(article_id, int):
                        article_id = str(article_id)
                    else:
                        article_id = article_id.encode("utf-8")
                    a_url = self.root_url + "/p/" + article_id + ".html"
                    a_time = item["published_at"].encode("utf-8")
                    if a_time < start_time:  # 如果文章太老了，停止搜索
                        return
                    elif a_time > end_time:  # 如果文章太新了，继续搜索，但不保存
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

                last_id = items[-1]["id"]
                if isinstance(last_id, int):
                    last_id = str(last_id)
                else:
                    last_id = last_id.encode("utf-8")

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
                strings = p.stripped_strings
                for string in strings:
                    a_text = a_text + string.encode('utf-8')
                a_text += "\n"
            # 标签
            a_tags = ""
            tags = data[
                "extraction_tags"]  # "extraction_tags": "[[\"早期项目\",\"zaoqixiangmu\",1],[\"信息安全\",\"xinxianquan\",2],[\"网络运维\",\"wangluoyunwei\",2]]"
            if tags is not None:
                tags = re.findall(u"[\u4e00-\u9fa5]+", tags)
                if len(tags) > 0:
                    a_tags = u" ".join(tags)
                    a_tags = a_tags.encode("utf-8")

            article = Article(a_title=a_title, a_text=a_text, a_time=a_time, a_author=a_author, a_url=a_url,
                              a_tags=a_tags)
            return article
        except urllib2.HTTPError, e:
            print "HTTPError:", e.code, e.reason
        except urllib2.URLError, e:
            print "URLError:", e.reason
        except:
            print "未知错误"
        return None


if __name__ == "__main__":
    crawler = Crawler36Kr(proj_name="article_xx")
    crawler.rebuild_table()
    crawler.crawl("2016-08-15 00:00:00", "2016-08-23 00:00:00")
