# coding=utf-8
import MySQLdb
import time
import os
import shutil


class Crawler:
    def __init__(self):
        self.name = "Crawler"
        self.root_url = "www.ruijie.com.cn"
        self.count = 0
        self.db = MySQLdb.connect(host="localhost", user="root", passwd="123456", db="test", charset='utf8')
        if not os.path.exists("articles/txt/"):
            os.makedirs("articles/txt/")
        if not os.path.exists("articles/attr/"):
            os.makedirs("articles/attr/")

    def crawl(self, end_time, start_time=None):
        pass

    def save(self, article):
        print(str(self.count) + " " + article.a_time + " " + article.a_title + " " + article.a_url)

        # 相关信息写入数据库(time, url)
        try:
            cursor = self.db.cursor()
            sql = """insert into article (url, time) values ('%s', '%s')""" % (article.a_url, article.a_time)
            cursor.execute(sql)
            self.db.commit()

            sql = "select last_insert_id()"
            cursor.execute(sql)
            results = cursor.fetchall()
            id = results[0][0]
        except:
            self.db.rollback()

        # 相关信息写入文件(time, url, tags, text, title, author)
        file_name = "articles/txt/%d" % id
        doc_text = open(file_name, 'w')
        doc_text.write(article.a_title + "\n" + article.a_tags + "\n" + article.a_text)
        doc_text.close()

        file_name = "articles/attr/%d" % id
        doc_attr = open(file_name, 'w')
        doc_attr.write(article.a_time + "\n" + article.a_title + "\n" + article.a_url + "\n" + article.a_tags)
        doc_attr.close()

    def delete_all_data(self):
        # 删除表内容
        cursor = self.db.cursor()
        cursor.execute("DROP TABLE IF EXISTS ARTICLE")
        sql = """CREATE TABLE ARTICLE (
                 ID INT AUTO_INCREMENT PRIMARY KEY,
                 URL VARCHAR(1000),
                 TIME DATETIME )"""
        cursor.execute(sql)

        # 删除文章
        shutil.rmtree("articles/txt/")
        shutil.rmtree("articles/attr/")

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


class Article:
    def __init__(self, a_title, a_text, a_author, a_url, a_time, a_tags):
        self.a_title = a_title
        self.a_text = a_text
        self.a_author = a_author
        self.a_url = a_url
        self.a_time = a_time
        self.a_tags = a_tags