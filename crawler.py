# coding=utf-8
import MySQLdb
import time
import os
import shutil
from myutils import Article


class Crawler:
    def __init__(self, proj_name):
        self.name = "Crawler"
        self.root_url = "www.ruijie.com.cn"
        self.proj_name = proj_name
        self.count = 0
        self.db = MySQLdb.connect(host="localhost", user="root", passwd="123456", db="test", charset='utf8')
        self.txt_dir = "%s/txt" % self.proj_name
        self.attr_dir = "%s/attr" % self.proj_name
        if not os.path.exists(self.txt_dir):
            os.makedirs(self.txt_dir)
        if not os.path.exists(self.attr_dir):
            os.makedirs(self.attr_dir)

    def crawl(self, end_time, start_time=None):
        pass

    def save(self, article):
        print(str(self.count) + " " + article.a_time + " " + article.a_title + " " + article.a_url)

        # 相关信息写入数据库(time, url)
        try:
            cursor = self.db.cursor()
            sql = """insert into %s (url, time) values ('%s', '%s')""" % (self.proj_name, article.a_url, article.a_time)
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

        # 删除文章
        shutil.rmtree(self.txt_dir)
        shutil.rmtree(self.attr_dir)

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
