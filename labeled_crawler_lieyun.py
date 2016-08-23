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


# 虎嗅爬虫
class LabeledCrawlerLieyun(LabeledCrawler):
    def __init__(self, proj_name):
        LabeledCrawler.__init__(self, proj_name)
        self.name = "猎云网"
        self.root_url = "http://www.lieyunwang.com"

    def crawl(self, start_time, end_time):
        self.labeled_crawl("http://www.lieyunwang.com/d/computing", 3466, start_time, end_time, self.cat_dict["智能硬件"])
        self.labeled_crawl("http://www.lieyunwang.com/d/vrar", 26936, start_time, end_time, self.cat_dict["VR"])
        self.labeled_crawl("http://www.lieyunwang.com/d/jiaoyu", 27669, start_time, end_time, self.cat_dict["教育"])
        self.labeled_crawl("http://www.lieyunwang.com/d/jinrong", 27670, start_time, end_time, self.cat_dict["互联网金融"])
        self.labeled_crawl("http://www.lieyunwang.com/d/qiche", 27671, start_time, end_time, self.cat_dict["汽车"])
        self.labeled_crawl("http://www.lieyunwang.com/d/fangchan", 27673, start_time, end_time, self.cat_dict["房产"])
        self.labeled_crawl("http://www.lieyunwang.com/d/yiliao", 27674, start_time, end_time, self.cat_dict["医疗健康"])
        self.labeled_crawl("http://www.lieyunwang.com/d/lvyou", 27675, start_time, end_time, self.cat_dict["旅游"])
        self.labeled_crawl("http://www.lieyunwang.com/d/shenghuo", 27676, start_time, end_time, self.cat_dict["O2O"])
        self.labeled_crawl("http://www.lieyunwang.com/d/qiyefuwu", 27677, start_time, end_time, self.cat_dict["企业服务"])
        self.labeled_crawl("http://www.lieyunwang.com/d/zhineng", 27678, start_time, end_time, self.cat_dict["人工智能"])
        self.labeled_crawl("http://www.lieyunwang.com/d/yule", 27680, start_time, end_time, self.cat_dict["娱乐"])
        self.labeled_crawl("http://www.lieyunwang.com/d/tiyu", 27682, start_time, end_time, self.cat_dict["体育"])
        self.labeled_crawl("http://www.lieyunwang.com/d/shejiao", 27683, start_time, end_time, self.cat_dict["社交"])
        self.labeled_crawl("http://www.lieyunwang.com/d/dianshang", 27684, start_time, end_time, self.cat_dict["电商"])
        self.labeled_crawl("http://www.lieyunwang.com/d/wuliu", 27685, start_time, end_time, self.cat_dict["物流"])
        self.labeled_crawl("http://www.lieyunwang.com/d/gongju", 27686, start_time, end_time, self.cat_dict["工具"])

    def labeled_crawl(self, start_url, cid, start_time, end_time, a_category):
        try:
            # 初次加载
            last_time = None
            html = urllib2.urlopen(start_url).read()
            soup = BeautifulSoup(html, "lxml")
            ul = soup.find(name="div", class_="article-box").ul
            lis = ul.find_all(name="li", recursive=False)

            for li in lis:
                a_url = self.root_url + li.a["href"]
                a_time = li["post_date"]
                if a_time < start_time:  # 如果文章太老了，停止搜索
                    return
                elif a_time > end_time: # 如果文章太新了，继续搜索
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
            last_time = lis[-1]["post_date"]

            # 加载更多
            while True:
                url = "http://www.lieyunwang.com/api/v1/posts?\
                starttime=%s&cid=%d&keyword=&tag=&searchcontent=&\
                scroll=true&scrollTo=100&title_remove_dujia=1" % (last_time, cid)
                html = urllib2.urlopen(url).read()
                json_obj = json.loads(html)
                articles = json_obj["content"]
                if len(articles) == 0:
                    return

                for article in articles:
                    a_url = article["postUrl"].encode("utf-8")
                    a_time = article["post_date"].encode("utf-8")
                    if a_time < start_time:  # 如果文章太老了，停止搜索
                        return
                    elif a_time > end_time: # 如果文章太新了，继续搜索
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
                last_time = articles[-1]["post_date"].encode("utf-8")
        except urllib2.HTTPError, e:
            print "HTTPError:", e.code, e.reason
        except urllib2.URLError, e:
            print "URLError:", e.reason
        except:
            print "未知错误"

    # 分析html, 返回Article对象
    def parse_html(self, a_url, a_time, a_category):
        # time.sleep(5)
        try:
            html = urllib2.urlopen(a_url).read()
            soup = BeautifulSoup(html, "lxml")
            div = soup.find(name="div", class_="bbbox clearfix").div.div.div
            # 标题
            a_title = ""
            strings = div.h1.stripped_strings
            for string in strings:
                a_title += string.encode("utf-8")
            # 作者，时间
            a_author = div.div.find_all(name="span", recursive=False)[1].span.string.encode('utf-8')
            # 正文
            a_text = ""
            plist = div.find(name="div", class_="main-text").find_all(name="p", recursive=False)
            for p in plist:
                if p.string is not None:
                    a_text = a_text + p.string.encode('utf-8') + "\n"
            # 标签
            a_tags = ""
            div_tags = div.find(name="div", class_="article-tag")
            if div_tags is not None:
                alist = div_tags.ul.find_all(name="a")
            else:
                alist = []
            if len(alist) > 0:
                alist = [a.string.encode('utf-8') for a in alist]
                a_tags = " ".join(alist)

            article = Article(a_title=a_title, a_text=a_text, a_time=a_time, a_author=a_author, a_url=a_url, a_tags=a_tags, a_category=a_category)
            return article
        except urllib2.HTTPError, e:
            print "HTTPError:", e.code, e.reason
        except urllib2.URLError, e:
            print "URLError:", e.reason
        except:
            print "未知错误"
        return None

if __name__ == "__main__":
    crawler = LabeledCrawlerLieyun(proj_name="article_cat")
    crawler.rebuild_table()
    crawler.crawl("2016-08-06 00:00:00", "2016-08-23 23:59:59")
