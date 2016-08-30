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
from gensim import utils
from gensim.models.doc2vec import LabeledSentence, TaggedDocument, TaggedLineDocument
from gensim.models import Doc2Vec
import numpy
from random import shuffle
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from articledb import ArticleDB


class TextClassifierTfidf:
    def __init__(self, project_name):
        self.project_name = project_name
        self.texts = None
        self.labels = None
        self.vect = CountVectorizer()
        self.tfidf = TfidfTransformer()
        self.clf = SGDClassifier()
        self.pipeline = Pipeline([
            ('vect', self.vect),
            ('tfidf', self.tfidf),
            ('clf', self.clf)])
        self.pipeline_transform = Pipeline([
            ('vect', self.vect),
            ('tfidf', self.tfidf)])

    def train(self):
        db = ArticleDB()
        # 导入数据
        corpus_name = self.project_name + "/seg_join/corpus.txt"
        with open(corpus_name, "r") as corpus:
            self.texts = corpus.readlines()
        sql = "select id, category from %s" % self.project_name
        results = db.execute(sql)
        db.close()
        self.labels = [row[1] for row in results]

        # 切分训练数据和测试数据
        x = self.texts
        y = self.labels
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=1)

        # 训练
        self.pipeline.fit(x_train, y_train)

        # 测试
        y_pred = self.pipeline.predict(x_test)
        print(metrics.classification_report(y_test, y_pred))

    def predict(self, x):
        return self.pipeline.predict(x)

    def transform(self, x):
        return self.pipeline_transform.transform(x)


class TextClassifierDoc2Vec:
    def __init__(self, project_name):
        self.project_name = project_name
        self.clf = SVC()

    def train(self):
        # 导入数据
        db = ArticleDB()
        # 训练doc2vec
        corpus_name = self.project_name + "/seg_join/corpus.txt"
        # model = Doc2Vec(min_count=1, window=10, size=400, sample=1e-4, negative=5, workers=8)
        # sources = {corpus_name: 'TRAIN'}
        # sentences = LabeledLineSentence(sources)
        # model.build_vocab(sentences.to_array())
        # for epoch in range(10):
        #     model.train(sentences.sentences_perm())
        # model.save('./news.d2v')
        model = Doc2Vec.load('./news.d2v')

        # 切分训练数据和测试数据
        results = db.execute("select id, category from %s" % self.project_name)
        y = [row[1] for row in results]
        results = db.execute("select count(id) from %s" % self.project_name)
        doc_num = results[0][0]
        db.close()
        x = [model.docvecs["TRAIN_%d" % i] for i in range(doc_num)]
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=1)

        # 训练
        self.clf.fit(x_train, y_train)

        # 测试
        y_pred = self.clf.predict(x_test)
        print(metrics.classification_report(y_test, y_pred))

    def predict(self, x):
        return self.clf.predict(x)

    def transform(self, x):
        return self.clf.transform(x)


class LabeledLineSentence(object):
    def __init__(self, sources):
        self.sentences = []
        self.sources = sources
        flipped = {}
        # make sure that keys are unique
        for key, value in sources.items():
            if value not in flipped:
                flipped[value] = [key]
            else:
                raise Exception('Non-unique prefix encountered')

    def __iter__(self):
        for source, prefix in self.sources.items():
            with utils.smart_open(source) as fin:
                for item_no, line in enumerate(fin):
                    yield TaggedDocument(utils.to_unicode(line).split(), [prefix + '_%d' % item_no])

    def to_array(self):
        self.sentences = []
        for source, prefix in self.sources.items():
            with utils.smart_open(source) as fin:
                for item_no, line in enumerate(fin):
                    # self.sentences.append(TaggedDocument(utils.to_unicode(line).split(), [prefix + '_%s' % item_no]))
                    self.sentences.append(TaggedDocument(utils.to_unicode(line).split(), [unicode(prefix + '_%s' % item_no)]))
        return self.sentences

    def sentences_perm(self):
        shuffle(self.sentences)
        return self.sentences


if __name__ == "__main__":
    clf = TextClassifierDoc2Vec(project_name="article_cat")
    clf.train()
