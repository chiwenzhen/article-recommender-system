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
class CrawlerKanchai(Crawler):
    def __init__(self, proj_name):
        Crawler.__init__(self, proj_name)
        self.name = "砍柴网"
        self.root_url = "http://www.ikanchai.com/"

    def crawl(self, start_time, end_time):
        try:
            # 初次加载
            html = urllib2.urlopen("http://www.ikanchai.com/").read()
            soup = BeautifulSoup(html, "lxml")
            ul = soup.find(name="div", class_="hlrmtj-content").ul
            lis = ul.find_all(name="li", class_="rtmj-box")
            for li in lis:
                a = li.dl.dt.a
                a_url = a["href"]
                str_time = a.img["src"][-17:-7]
                a_time = self.time_num2str(float(str_time))
                if a_time < start_time:  # 如果文章太老了，停止搜索
                    return
                elif a_time > end_time:  # 如果文章太新了，继续搜索
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

            # 加载更多
            page = 1
            while True:
                page += 1
                html = urllib2.urlopen(
                    "http://app.ikanchai.com/roll.php?do=more&sectionid=255&status=1&sort=0&\
                    pagesize=5&page=%d&callback=jQuery191003956674294513696_1471875660022&\
                    Name=keyun&_=1471875660026" % page).read()[42:-1]
                json_obj = json.loads(html)
                data = json_obj["data"]
                for item in data:
                    a_url = item["url"].encode("utf-8")
                    a_time = self.time_num2str(float(item["thumb"][-17:-7].encode("utf-8")))
                    if a_time < start_time:  # 如果文章太老了，停止搜索
                        return
                    elif a_time > end_time:  # 如果文章太新了，继续搜索
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
        try:
            html = urllib2.urlopen(a_url).read()
            soup = BeautifulSoup(html, "lxml")
            div_hl_content = soup.find(name="div", class_="hl_content")
            # 标题
            a_title = div_hl_content.find(name="div", class_="hl_c_title").h2.contents[0].encode("utf-8")
            # 作者，时间
            #a_author = div_hl_content.find(name="div", class_="hl_c_twid").a.stripped_string
            a_author = "暂未提取"
            a_time = a_time
            # 正文
            a_text = ""
            plist = div_hl_content.find(name="div", class_="hl_body").find_all(name="p")
            for p in plist:
                if p.string is not None:
                    a_text = a_text + p.string.encode('utf-8') + "\n"
            # 标签
            a_tags = ""
            div_hl_c_tagl = div_hl_content.find(name="div", class_="hl_c_tagl")

            if div_hl_c_tagl is not None:
                lis = div_hl_c_tagl.ul.find_all(name="li")
            else:
                alist = []
            if len(lis) > 0:
                alist = [li.a.string.encode('utf-8') for li in lis]
                a_tags = " ".join(alist)

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
    crawler = CrawlerKanchai("article_xxx")
    crawler.rebuild_table()
    crawler.crawl("2016-08-15 00:00:00", "2016-08-23 23:59:59")
