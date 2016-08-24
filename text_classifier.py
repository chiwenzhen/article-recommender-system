# coding=utf-8
import MySQLdb
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline
from sklearn.cross_validation import train_test_split
from sklearn.linear_model.logistic import LogisticRegression
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn import metrics
import numpy as np


class TextClassifier:
    def __init__(self, project_name):
        self.project_name = project_name
        self.texts = None
        self.labels = None
        self.pipeline = Pipeline([
            ('vect', CountVectorizer()),
            ('tfidf', TfidfTransformer()),
            ('clf', SGDClassifier())])

    def test(self):
        # 导入数据
        corpus_name = self.project_name + "/seg_join/corpus.txt"
        with open(corpus_name, "r") as corpus:
            self.texts = corpus.readlines()
        db = MySQLdb.connect(host="localhost", user="root", passwd="123456", db="test", charset='utf8')
        cursor = db.cursor()
        sql = "select id, category from article_cat"
        cursor.execute(sql)
        results = cursor.fetchall()
        self.labels = [row[1] for row in results]

        # 切分训练数据和测试数据
        x = self.texts
        y = self.labels
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=1)


        # debug code


        # 训练
        self.pipeline.fit(x_train, y_train)

        # 测试
        y_pred = self.pipeline.predict(x_test)
        print(metrics.classification_report(y_test, y_pred))

if __name__ == "__main__":
    clf = TextClassifier(project_name="article_cat")
    clf.test()

