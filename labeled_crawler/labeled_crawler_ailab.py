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


# 二级分类 for 人工智能
class LabeledCrawlerAilab(LabeledCrawler):
    def __init__(self, proj_name):
        LabeledCrawler.__init__(self, proj_name)
        self.name = "AI实验室"
        self.root_url = "http://www.ailab.cn"

    def crawl(self, start_time, end_time):
        self.labeled_crawl("http://www.ailab.cn/robot/list_8_", start_time, end_time, self.cat_dict["人工智能"], "机器学习")
        self.labeled_crawl("http://www.ailab.cn/Intelligent_Robots/list_49_", start_time, end_time, self.cat_dict["人工智能"], "机器人")
        self.labeled_crawl("http://www.ailab.cn/mode/voice/list_14_", start_time, end_time, self.cat_dict["人工智能"], "语音识别")
        self.labeled_crawl("http://www.ailab.cn/robot/language/list_16_", start_time, end_time, self.cat_dict["人工智能"], "NLP")
        self.labeled_crawl("http://www.ailab.cn/mode/char/list_13_", start_time, end_time, self.cat_dict["人工智能"], "字符识别")
        self.labeled_crawl("http://www.ailab.cn/mode/fingerprint/list_18_", start_time, end_time, self.cat_dict["人工智能"], "指纹识别")
        self.labeled_crawl("http://www.ailab.cn/mode/face/list_19_", start_time, end_time, self.cat_dict["人工智能"], "人脸识别")
        self.labeled_crawl("http://www.ailab.cn/robot/search/list_17_", start_time, end_time, self.cat_dict["人工智能"], "搜索引擎")
        self.labeled_crawl("http://www.ailab.cn/algorithm/neuralnetwork/list_24_", start_time, end_time, self.cat_dict["人工智能"], "神经网络")
        self.labeled_crawl("http://www.ailab.cn/datamining/list_30_", start_time, end_time, self.cat_dict["人工智能"], "数据挖掘")
        self.labeled_crawl("http://www.ailab.cn/rfid/house/list_52_", start_time, end_time, self.cat_dict["智能硬件"], "智能家居")
        self.labeled_crawl("http://www.ailab.cn/rfid/smartdevice/list_56_", start_time, end_time, self.cat_dict["智能硬件"], "可穿戴")
        self.labeled_crawl("http://www.ailab.cn/uav/list_58_", start_time, end_time, self.cat_dict["智能硬件"], "无人机")
        self.labeled_crawl("http://www.ailab.cn/rfid/iov/list_55_", start_time, end_time, self.cat_dict["汽车"], "无人驾驶")
        self.labeled_crawl("http://www.ailab.cn/rfid/nfc/list_57_", start_time, end_time, self.cat_dict["互联网金融"], "移动支付")
        self.labeled_crawl("http://www.ailab.cn/cloud/list_33", start_time, end_time, self.cat_dict["企业服务"], "云计算")
        self.labeled_crawl("http://www.ailab.cn/datamining/list_30_", start_time, end_time, self.cat_dict["企业服务"], "大数据")

    def labeled_crawl(self, start_url, start_time, end_time, a_category, subcategory):
        try:
            page = 0
            while True:
                page += 1
                html = urllib2.urlopen("%s%d.html" % (start_url, page)).read()
                soup = BeautifulSoup(html, "lxml")
                div = soup.find(name="div", class_="listl list2")
                if div is None:
                    return
                lis = div.ul.find_all(name="li", recursive=False)
                for li in lis:
                    a_url = self.root_url + li.h3.a["href"]
                    a_time = li.span.string[3:].encode("utf-8")
                    if a_time < start_time:  # 如果文章太老了，停止搜索
                        return
                    elif a_time > end_time:  # 如果文章太新了，继续搜索
                        continue
                    else:  # 如果文章在区间内，则分析文章，并继续搜索
                        # 解析文章html
                        article = self.parse_html(a_url, a_time, a_category, subcategory)
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
    def parse_html(self, a_url, a_time, a_category, subcategory):
        try:
            html = urllib2.urlopen(a_url, timeout=30).read()
            soup = BeautifulSoup(html, "lxml")
            div = soup.find(name="div", class_="inner")
            # 标题
            a_title = div.find(name="div", class_="listltitle").h3.string.encode("utf-8")
            # 作者，时间
            a_author = "暂未提取"
            # 正文
            a_text = ""
            plist = div.find(name="div", id="mainDiv").find_all(name="p")
            for p in plist:
                strings = p.stripped_strings
                for string in strings:
                    a_text = a_text + string.encode('utf-8')
                a_text += "\n"
            # 标签
            a_tags = subcategory

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
    crawler = LabeledCrawlerAilab(proj_name="article_cat")
    # crawler.rebuild_table()
    crawler.crawl("2010-08-10 00:00:00", "2016-10-23 23:59:59")
