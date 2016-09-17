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
class LabeledCrawlerBaidu(LabeledCrawler):
    def __init__(self, proj_name):
        LabeledCrawler.__init__(self, proj_name)
        self.name = "百度百家"
        self.root_url = "http://http://baijia.baidu.com/"

    def crawl(self, start_time, end_time):
        # VR
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=20104",
                           start_time, end_time, self.cat_dict["VR"])  # VR
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=25479",
                           start_time, end_time, self.cat_dict["VR"])  # AR
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=68474",
                           start_time, end_time, self.cat_dict["VR"])  # VR直播
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=28594",
                           start_time, end_time, self.cat_dict["VR"])  # VR游戏
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=36796",
                           start_time, end_time, self.cat_dict["VR"])  # VR电影

        # 人工智能
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=10523",
                           start_time, end_time, self.cat_dict["人工智能"])  # 人工智能
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=24133",
                           start_time, end_time, self.cat_dict["人工智能"])  # AI
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=16828",
                           start_time, end_time, self.cat_dict["人工智能"])  # 机器学习
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=20422",
                           start_time, end_time, self.cat_dict["人工智能"])  # 深度学习
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=67425",
                           start_time, end_time, self.cat_dict["人工智能"])  # 神经网络
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=19736",
                           start_time, end_time, self.cat_dict["人工智能"])  # NLP
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=105061",
                           start_time, end_time, self.cat_dict["人工智能"])  # 自然语言

        # 智能硬件
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=11254",
                           start_time, end_time, self.cat_dict["智能硬件"])  # 智能硬件
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=12630",
                           start_time, end_time, self.cat_dict["智能硬件"])  # 智能穿戴
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=11253",
                           start_time, end_time, self.cat_dict["智能硬件"])  # 可穿戴
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=12752",
                           start_time, end_time, self.cat_dict["智能硬件"])  # 机器人
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=10520",
                           start_time, end_time, self.cat_dict["智能硬件"])  # 无人机
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=20605",
                           start_time, end_time, self.cat_dict["智能硬件"])  # 飞行器
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=22625",
                           start_time, end_time, self.cat_dict["智能硬件"])  # 大疆
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=10492",
                           start_time, end_time, self.cat_dict["智能硬件"])  # 智能电视
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=11478",
                           start_time, end_time, self.cat_dict["智能硬件"])  # 智能家居

        # 游戏直播
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=10234",
                           start_time, end_time, self.cat_dict["游戏&直播"])  # 游戏
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=11459",
                           start_time, end_time, self.cat_dict["游戏&直播"])  # 手机游戏
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=10179",
                           start_time, end_time, self.cat_dict["游戏&直播"])  # 手游
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=10309",
                           start_time, end_time, self.cat_dict["游戏&直播"])  # 页游
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=10375",
                           start_time, end_time, self.cat_dict["游戏&直播"])  # 网游
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=12764",
                           start_time, end_time, self.cat_dict["游戏&直播"])  # 直播

        # 物联网
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=14131",
                           start_time, end_time, self.cat_dict["物联网"])  # 物联网
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=10948",
                           start_time, end_time, self.cat_dict["物联网"])  # 车联网
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=14706",
                           start_time, end_time, self.cat_dict["物联网"])  # 传感器

        # 医疗健康
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=14671",
                           start_time, end_time, self.cat_dict["医疗健康"])  # 移动医疗
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=18591",
                           start_time, end_time, self.cat_dict["医疗健康"])  # 医药电商
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=15453",
                           start_time, end_time, self.cat_dict["医疗健康"])  # 医药
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=48667",
                           start_time, end_time, self.cat_dict["医疗健康"])  # 医疗器械
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=24459",
                           start_time, end_time, self.cat_dict["医疗健康"])  # 医疗设备
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=19950",
                           start_time, end_time, self.cat_dict["医疗健康"])  # 远程医疗
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=39196",
                           start_time, end_time, self.cat_dict["医疗健康"])  # 精准医疗

        # 教育
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=13378",
                           start_time, end_time, self.cat_dict["教育"])  # 在线教育
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=13857",
                           start_time, end_time, self.cat_dict["教育"])  # k12

        # 互联网金融
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=11765",
                           start_time, end_time, self.cat_dict["互联网金融"])  # 金融
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=35148",
                           start_time, end_time, self.cat_dict["互联网金融"])  # 区块链
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=10232",
                           start_time, end_time, self.cat_dict["互联网金融"])  # 比特币
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=10971",
                           start_time, end_time, self.cat_dict["互联网金融"])  # P2P
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=14716",
                           start_time, end_time, self.cat_dict["互联网金融"])  # 保险
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=10845",
                           start_time, end_time, self.cat_dict["互联网金融"])  # 支付
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=10849",
                           start_time, end_time, self.cat_dict["互联网金融"])  # 支付宝
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=13401",
                           start_time, end_time, self.cat_dict["互联网金融"])  # 微信支付
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=10886",
                           start_time, end_time, self.cat_dict["互联网金融"])  # 移动支付

        # 手机
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=10180",
                           start_time, end_time, self.cat_dict["手机"])  # 手机
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=10122",
                           start_time, end_time, self.cat_dict["手机"])  # 智能手机
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=10147",
                           start_time, end_time, self.cat_dict["手机"])  # 小米
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=10255",
                           start_time, end_time, self.cat_dict["手机"])  # 苹果
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=10189",
                           start_time, end_time, self.cat_dict["手机"])  # 华为
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=11023",
                           start_time, end_time, self.cat_dict["手机"])  # 三星
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=21805",
                           start_time, end_time, self.cat_dict["手机"])  # OPPO
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=21821",
                           start_time, end_time, self.cat_dict["手机"])  # VIVO
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=16993",
                           start_time, end_time, self.cat_dict["手机"])  # 联想手机
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=12291",
                           start_time, end_time, self.cat_dict["手机"])  # 摩托罗拉
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=10339",
                           start_time, end_time, self.cat_dict["手机"])  # 魅族
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=19000",
                           start_time, end_time, self.cat_dict["手机"])  # LG

        # 企业服务
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=23832",
                           start_time, end_time, self.cat_dict["企业服务"])  # 企业服务
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=11033",
                           start_time, end_time, self.cat_dict["企业服务"])  # 大数据
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=18805",
                           start_time, end_time, self.cat_dict["企业服务"])  # SAAS
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=25356",
                           start_time, end_time, self.cat_dict["企业服务"])  # PaaS
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=19169",
                           start_time, end_time, self.cat_dict["企业服务"])  # IaaS
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=24655",
                           start_time, end_time, self.cat_dict["企业服务"])  # 容器
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=23886",
                           start_time, end_time, self.cat_dict["企业服务"])  # Dokcer
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=34634",
                           start_time, end_time, self.cat_dict["企业服务"])  # 超融合
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=22081",
                           start_time, end_time, self.cat_dict["企业服务"])  # 共享经济
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=16802",
                           start_time, end_time, self.cat_dict["企业服务"])  # b2b
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=13696",
                           start_time, end_time, self.cat_dict["企业服务"])  # 招聘

        # 汽车
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=10946",
                           start_time, end_time, self.cat_dict["汽车"])  # 汽车
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=22659",
                           start_time, end_time, self.cat_dict["汽车"])  # 自动驾驶
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=19295",
                           start_time, end_time, self.cat_dict["汽车"])  # 无人驾驶
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=11214",
                           start_time, end_time, self.cat_dict["汽车"])  # 智能汽车
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=13360",
                           start_time, end_time, self.cat_dict["汽车"])  # 电动汽车
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=10945",
                           start_time, end_time, self.cat_dict["汽车"])  # 特斯拉
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=17041",
                           start_time, end_time, self.cat_dict["汽车"])  # 租车
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=25060",
                           start_time, end_time, self.cat_dict["汽车"])  # 专车
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=17298",
                           start_time, end_time, self.cat_dict["汽车"])  # 二手车

        # 电商
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=10139",
                           start_time, end_time, self.cat_dict["电商"])  # 电商
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=10225",
                           start_time, end_time, self.cat_dict["电商"])  # 电子商务
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=20846",
                           start_time, end_time, self.cat_dict["电商"])  # 跨境电商
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=12090",
                           start_time, end_time, self.cat_dict["电商"])  # 零售
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=10208",
                           start_time, end_time, self.cat_dict["电商"])  # 垂直电商

        # O2O
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=10589",
                           start_time, end_time, self.cat_dict["O2O"])  # O2O
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=20983",
                           start_time, end_time, self.cat_dict["O2O"])  # 外卖
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=20587",
                           start_time, end_time, self.cat_dict["O2O"])  # 生鲜
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=20855",
                           start_time, end_time, self.cat_dict["O2O"])  # 家装
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=19996",
                           start_time, end_time, self.cat_dict["O2O"])  # 社区

        # 创投
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=13018",
                           start_time, end_time, self.cat_dict["创投"])  # 创投
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=10104",
                           start_time, end_time, self.cat_dict["创投"])  # 创业
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=24743",
                           start_time, end_time, self.cat_dict["创投"])  # 投融资
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=10999",
                           start_time, end_time, self.cat_dict["创投"])  # 投资
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=11446",
                           start_time, end_time, self.cat_dict["创投"])  # 融资

        # 评测
        self.labeled_crawl("http://baijia.baidu.com/?tn=listarticle&labelid=17760",
                           start_time, end_time, self.cat_dict["评测"])  # 评测



    def labeled_crawl(self, start_url, start_time, end_time, a_category):
        time.sleep(3)
        try:
            # 初次加载
            html = urllib2.urlopen(start_url).read()
            soup = BeautifulSoup(html, "lxml")
            divs = soup.find(name="div", class_="feeds").find_all(name="div", recursive=False)
            label_id = start_url[start_url.rfind("=") + 1:]

            for div in divs:
                a_url = div.h3.a["href"]
                a_time = div.find(name="span", class_="tm").string.encode("utf-8")
                a_time = self.get_format_time(a_time)
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
            last_id = divs[-1]["id"][5:]

            # 加载更多
            page = 1
            while True:
                page += 1
                url = "http://baijia.baidu.com/ajax/labellatestarticle?page=%d&pagesize=20&labelid=%s&prevarticalid=%s" % (page, label_id, last_id)
                html = urllib2.urlopen(url).read()
                json_obj = json.loads(html)
                if json_obj["data"]["total"] == 0:
                    return
                articles = json_obj["data"]["list"]


                for article in articles:
                    a_url = article["m_display_url"].encode("utf-8")
                    a_time = article["m_create_time"].encode("utf-8")
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
                last_id = articles[-1]["ID"].encode("utf-8")
        except urllib2.HTTPError, e:
            print "HTTPError:", e.code, e.reason
        except urllib2.URLError, e:
            print "URLError:", e.reason
        except:
            print "未知错误"

    # 分析html, 返回Article对象
    def parse_html(self, a_url, a_time, a_category):
        time.sleep(1)
        try:
            html = urllib2.urlopen(a_url, timeout=30).read()
            soup = BeautifulSoup(html, "lxml")
            div = soup.find(name="div", id="page")
            # 标题
            a_title = ""
            strings = div.h1.stripped_strings
            for string in strings:
                a_title += string.encode("utf-8")
            # 作者，时间
            a_author = ""
            a_time = div.div.div.span.string.encode("utf-8")
            a_time = time.strftime('%Y', time.localtime(time.time())) + "年" + a_time
            a_time = self.time_normalize(a_time, '%Y年%m月%d日 %H:%M')
            # 正文
            a_text = ""
            plist = div.find(name="div", class_="article-detail").find_all(name="p", recursive=False)
            for p in plist:
                strings = p.stripped_strings
                for string in strings:
                    a_text = a_text + string.encode('utf-8')
                a_text += "\n"
            # 标签
            a_tags = ""
            div_tags = div.div.find_all(name="div", recursive=False)[1]
            if div_tags is not None:
                alist = div_tags.find_all(name="a")
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

    # 返回完整的时间格式
    def get_format_time(self, str_time):
        if ":" in str_time:
            return "%s %s" % (time.strftime('%Y-%m-%d', time.localtime(time.time())), str_time)
        elif "-" in str_time:
            return "%s-%s 12:00:00" % (time.strftime('%Y', time.localtime(time.time())), str_time)
        else:
            print "时间格式不明: " + str_time


if __name__ == "__main__":
    crawler = LabeledCrawlerBaidu(proj_name="article_cat")
    # crawler.rebuild_table()
    crawler.crawl("2015-08-01 00:00:00", "2016-10-01 23:59:59")
