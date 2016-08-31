# coding=utf-8
import MySQLdb
import time
import os
import shutil
from myutils import Article


class LabeledCrawler:
    def __init__(self, proj_name):
        self.proj_name = proj_name
        self.name = "Root Crawler"
        self.root_url = "RootCrawler.com"
        self.count = 0

        self.db = MySQLdb.connect(host="localhost", user="root", passwd="123456", db="test", charset='utf8')

        self.txt_dir = self.proj_name + "/txt"
        self.attr_dir = self.proj_name + "/attr"
        self.seg_dir = self.proj_name + "/seg"
        self.seg_join_dir = self.proj_name + "/seg_join"
        self.dirs = [self.txt_dir, self.attr_dir, self.seg_dir, self.seg_join_dir]
        for d in self.dirs:
            if not os.path.exists(d): os.makedirs(d)

        self.cat_dict = {"VR": 1,
                         "人工智能": 2,
                         "智能硬件": 3,
                         "游戏&直播": 4,
                         "物联网": 5,
                         "医疗健康": 6,
                         "教育": 7,
                         "互联网金融": 8,
                         "手机": 9,
                         "企业服务": 10,
                         "汽车": 11,
                         "电商": 12,
                         "O2O": 13,
                         "资本": 14,
                         "旅游": 15,
                         "评测": 16,
                         "物流": 17,
                         "体育": 18,
                         "农业": 19,
                         "社交": 20,
                         "工具": 21,
                         "娱乐": 22,
                         "家居": 23,
                         "文创": 24,
                         "房产": 25,
                         "其他": 26,
                         }
        self.cat_rdict = {}
        for key, value in self.cat_dict.items():
            self.cat_rdict[value] = key

    def crawl(self, end_time, start_time=None):
        pass

    def save(self, article):
        print(str(self.count) + " " + article.a_time + " " + article.a_title + " " + article.a_url)

        # 相关信息写入数据库(time, url)
        try:
            cursor = self.db.cursor()
            sql = """insert into %s (url, time, category) values ('%s', '%s', %d)""" % (
                self.proj_name, article.a_url, article.a_time, article.a_category)
            cursor.execute(sql)
            self.db.commit()

            sql = "select last_insert_id()"
            cursor.execute(sql)
            results = cursor.fetchall()
            nexi_id = results[0][0]

            # 相关信息写入文件(time, url, tags, text, title, author)
            file_name = "%s/%d" % (self.txt_dir, nexi_id)
            doc_text = open(file_name, 'w')
            doc_text.write(article.a_title + "\n" + article.a_tags + "\n" + article.a_text)
            doc_text.close()

            file_name = "%s/%d" % (self.attr_dir, nexi_id)
            doc_attr = open(file_name, 'w')
            doc_attr.write(article.a_time + "\n" + article.a_title + "\n" + article.a_url + "\n" + article.a_tags + "\n")
            doc_attr.close()
        except:
            self.db.rollback()

    def rebuild_table(self):
        # 删除表内容
        cursor = self.db.cursor()
        cursor.execute("DROP TABLE IF EXISTS %s" % self.proj_name)
        sql = """CREATE TABLE %s (
                 ID INT AUTO_INCREMENT PRIMARY KEY,
                 URL VARCHAR(1000),
                 TIME DATETIME,
                 CATEGORY TINYINT)""" % self.proj_name
        cursor.execute(sql)

        # 删除数据
        for d in self.dirs:
            shutil.rmtree(d)

    # 时间转换：从字符串形式转浮点数，比如time_str2num("2011-09-28 10:00:00", "%Y-%m-%d %H:%M:%S")返回1317091800.0
    @staticmethod
    def time_str2num(str_time, time_format='%Y-%m-%d %H:%M:%S'):
        return time.mktime(time.strptime(str_time, time_format))

    # 时间转换：浮点数转换成字符串形式：1317091800.0->"2011-09-28 10:00:00"
    @staticmethod
    def time_num2str(ftime):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ftime))

    # 将各种格式的时间转换成统一格式：2011-09-28 10:23:35
    @staticmethod
    def time_normalize(str_time, time_format='%Y-%m-%d %H:%M:%S'):
        ftime = time.mktime(time.strptime(str_time, time_format))
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ftime))

    def __del__(self):
        self.db.close()
