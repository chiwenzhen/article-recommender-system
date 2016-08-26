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
class LabeledCrawlerYiou(LabeledCrawler):
    def __init__(self, proj_name):
        LabeledCrawler.__init__(self, proj_name)
        self.name = "亿欧网"
        self.root_url = "http://www.iyiou.com/"

    def crawl(self, start_time, end_time):
        self.labeled_crawl("http://auto.iyiou.com/", start_time, end_time, self.cat_dict["汽车"])
        self.labeled_crawl("http://ret.iyiou.com/", start_time, end_time, self.cat_dict["电商"])
        self.labeled_crawl("http://fin.iyiou.com/", start_time, end_time, self.cat_dict["互联网金融"])
        self.labeled_crawl("http://med.iyiou.com/", start_time, end_time, self.cat_dict["医疗健康"])
        # self.labeled_crawl("http://est.iyiou.com/", start_time, end_time, self.cat_dict["房产"])
        # self.labeled_crawl("http://phy.iyiou.com/", start_time, end_time, self.cat_dict["体育"])
        # self.labeled_crawl("http://win.iyiou.com/", start_time, end_time, self.cat_dict["文创"])
        self.labeled_crawl("http://tech.iyiou.com/", start_time, end_time, self.cat_dict["智能硬件"])
        self.labeled_crawl("http://www.iyiou.com/i/canyin/", start_time, end_time, self.cat_dict["O2O"])
        # self.labeled_crawl("http://www.iyiou.com/i/lvyou/", start_time, end_time, self.cat_dict["旅游"])
        self.labeled_crawl("http://www.iyiou.com/i/jiaoyu/", start_time, end_time, self.cat_dict["教育"])
        # self.labeled_crawl("http://www.iyiou.com/i/jiaju/", start_time, end_time, self.cat_dict["O2O"])
        # self.labeled_crawl("http://www.iyiou.com/i/shengxian/", start_time, end_time, self.cat_dict["O2O"])
        # self.labeled_crawl("http://www.iyiou.com/i/B2B/", start_time, end_time, self.cat_dict["企业服务"])

    def labeled_crawl(self, start_url, start_time, end_time, a_category):
        try:
            page = 0
            while True:
                page += 1
                html = urllib2.urlopen("%spage/%d.html" % (start_url, page)).read()
                soup = BeautifulSoup(html, "lxml")
                div_post = soup.find(name="div", id="post_list")
                divs = div_post.find_all(name="div", class_="post", recursive=False)
                if len(divs) == 0:
                    return

                for div in divs:
                    div_right = div.find(name="div", class_="post_right")
                    a_url = div_right.h1.a["href"]
                    a_time = div_right.div.find(name="div", class_="post_date").string.encode("utf-8")
                    a_time = self.restore_time(a_time)
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

    def restore_time(self, str_time):
        now = time.time()
        if "分钟前" in str_time:
            str_time = str_time.replace("分钟前", "").strip()
            elapsed = int(str_time) * 60
        elif "小时前" in str_time:
            str_time = str_time.replace("小时前", "").strip()
            elapsed = int(str_time) * 3600
        elif "昨天" in str_time:
            hm = str_time[-5:]
            today = self.time_num2str(now)[:11]
            now = self.time_str2num(today+hm+":00")
            elapsed = 24 * 3600
        else:
            return str_time
        post_time = now - elapsed
        return self.time_num2str(post_time)


    # 分析html, 返回Article对象
    def parse_html(self, a_url, a_time, a_category):
        try:
            html = urllib2.urlopen(a_url, timeout=30).read()
            soup = BeautifulSoup(html, "lxml")
            div_post = soup.find(name="div", id="post_content")

            # 标题
            a_title = div_post.find(name="div", id="post_title").string.encode("utf-8")
            # 作者，时间
            a_author = div_post.find(name="div", id="post_info").\
                div.find(name="div",id="post_author").string.encode("utf-8")
            # 正文
            a_text = ""
            plist = div_post.find(name="div", id="post_description").find_all(name="p", recursive=False)
            for p in plist:
                strings = p.stripped_strings
                for string in strings:
                    a_text = a_text + string.encode('utf-8')
                a_text += "\n"
            # 标签
            a_tags = ""
            alist = div_post.find(name="div", class_="article_info_box").\
                find(name="div", class_="article_info_box_right").find_all(name="a")
            if alist is not None:
                alist = [a.string.encode('utf-8') for a in alist if a.string is not None]
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
    crawler = LabeledCrawlerYiou(proj_name="article_test")
    crawler.rebuild_table()
    crawler.crawl("2016-01-01 00:00:00", "2016-08-23 23:59:59")
