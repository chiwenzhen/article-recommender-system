# coding=utf-8
import heapq
import pickle
import MySQLdb
import re


# 文章结构
class Article:
    def __init__(self, a_title, a_text, a_url, a_time, a_tags, a_category=None, a_id=None, a_score=None, a_author=None):
        self.a_title = a_title
        self.a_text = a_text
        self.a_url = a_url
        self.a_time = a_time
        self.a_tags = a_tags
        self.a_category = a_category
        self.a_id = a_id
        self.a_score = a_score
        self.a_author = a_author

    def __lt__(self, other):
        return self.a_score < other.a_score

    def __gt__(self, other):
        return self.a_score > other.a_score

# 用于获取Top K数据的堆
class TopkHeap(object):
    def __init__(self, k):
        self.k = k
        self.data = []

    def push(self, elem):
        if len(self.data) < self.k:
            heapq.heappush(self.data, elem)
        else:
            topk_small = self.data[0]
            if topk_small < elem:
                heapq.heapreplace(self.data, elem)

    def topk(self):
        return [x for x in reversed([heapq.heappop(self.data) for x in xrange(len(self.data))])]


# 数据库连接
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


# 对象保存和载入
class Dumper:
    @staticmethod
    def save(obj, file_name):
        pickle.dump(obj, open(file_name, "wb"), True)

    @staticmethod
    def load(file_name):
        obj = pickle.load(open(file_name, "rb"))
        return obj


# 文章对象保存和载入
class ArticleDumper:
    def __init__(self, proj_name):
        self.proj_name = proj_name
        db = ArticleDB()
        self.doc_num = db.execute("select count(*) from %s" % self.proj_name)[0][0]
        db.close()

    def load(self, a_id):
        if a_id == -1:
            all_articles = []
            for i in xrange(self.doc_num):
                obj_name = self.proj_name + "/obj/" + str(i+1)
                article = Dumper.load(obj_name)
                all_articles.append(article)
            return all_articles
        else:
            obj_name = self.proj_name + "/obj/" + str(a_id)
            article = Dumper.load(obj_name)
            return article


# 文章类别
class Category:
    categories = [
        [1, "VR", "vr"],
        [2, "人工智能", "ai"],
        [3, "智能硬件", "hardware"],
        [4, "游戏&直播", "game"],
        [5, "物联网", "iot"],
        [6, "医疗健康", "medical"],
        [7, "教育", "education"],
        [8, "互联网金融", "finance"],
        [9, "手机", "mobile"],
        [10, "企业服务", "enterprise"],
        [11, "汽车", "car"],
        [12, "电商", "ecommerce"],
        [13, "O2O", "o2o"],
        [14, "资本", "capital"],
        [15, "旅游", "travel"],
        [16, "评测", "evaluation"],
        [17, "物流", "logistics"],
        [18, "体育", "sport"],
        [19, "农业", "agriculture"],
        [20, "社交", "sns"],
        [21, "工具", "tool"],
        [22, "娱乐", "entertainment"],
        [23, "家居", "furniture"],
        [24, "文创", "culture"],
        [25, "房产", "property"],
        [26, "其他", "others"]]

    def __init__(self):
        self.n2c = dict([(row[0], row[1]) for row in self.categories])
        self.n2e = dict([(row[0], row[2]) for row in self.categories])
        self.c2n = dict([(row[1], row[0]) for row in self.categories])
        self.c2e = dict([(row[1], row[2]) for row in self.categories])
        self.e2n = dict([(row[2], row[0]) for row in self.categories])
        self.e2c = dict([(row[2], row[1]) for row in self.categories])

# 停用词
class StopWord:
    def __init__(self, file_name):
        # 停用词表
        with open(file_name, 'r') as stop_file:
            self.stop_words = set([line.strip() for line in stop_file])

    # 判断词语是否要过滤：停用词，单字词，数字
    def is_stop_word(self, word):
        flag = word in self.stop_words \
               or re.match("[\d]+", word) \
               or len(word.decode("utf-8")) == 1
        return flag


# 分句符号
class StopSent:
    def __init__(self):
        self.delimiters = set(u"\u00a0＃[。，,！……!《》<>\"':：？\?、\|“”‘’；]{}（）{}【】()｛｝（）：？！。，;、~——+％%`:“”＂'‘\n\r")

    # 是否是分句符号 c为uicode编码，非utf-8、ascii等
    def is_delim(self, c):
        return c in self.delimiters

if __name__ == "__main__":
    stopsent = StopSent()
    print stopsent.is_delim(u"\u00a0".encode("utf-8"))
    print stopsent.is_delim("＃")
    print stopsent.is_delim("！")
    print stopsent.is_delim("<")