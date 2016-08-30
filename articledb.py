# coding=utf-8
import MySQLdb


class ArticleDB:
    def __init__(self):
        self.db = MySQLdb.connect(host="localhost", user="root", passwd="123456", db="test", charset='utf8')
        self.cursor = self.db.cursor()

    def execute(self, sql):
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
        except:
            self.db.rollback()
        return results

    def commit(self):
        self.db.commit()

    def close(self):
        self.db.close()
