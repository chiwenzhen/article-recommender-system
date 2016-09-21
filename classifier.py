# coding=utf-8
import MySQLdb
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, TfidfTransformer
from sklearn.decomposition import LatentDirichletAllocation
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
from myutils import ArticleDB, Dumper, StopWord, Category, FreqCharUtil, read_subcat
from sklearn.cluster import KMeans
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from collections import defaultdict, namedtuple
from sklearn.feature_selection import SelectKBest, chi2
import dill


class TextClassifierTfidf:
    def __init__(self, project_name):
        self.project_name = project_name
        self.texts = None
        self.labels = None
        self.tfidf = TfidfVectorizer()
        self.ch2 = SelectKBest(chi2, k=1000)
        self.clf = SGDClassifier()

        self.pipeline = Pipeline([
            ('tfidf', self.tfidf),
            ('chi2', self.ch2),
            ('clf', self.clf)])
        self.pipeline_transform = Pipeline([
            ('tfidf', self.tfidf),
            ('chi2', self.ch2)])

        # 使用lda主题分布作为分类依据，效果很差，准确率仅50%左右
        # self.tf = CountVectorizer()
        # self.lda = LatentDirichletAllocation(n_topics=10)
        # self.clf = LogisticRegression()
        #
        # self.pipeline = Pipeline([
        #     ('tf', self.tf),
        #     ('lda', self.lda),
        #     ('clf', self.clf)])
        # self.pipeline_transform = Pipeline([
        #     ('tf', self.tf),
        #     ('lda', self.lda)])

    def train(self):
        db = ArticleDB()
        # 导入数据
        print "reading corpus.txt ..."
        corpus_name = self.project_name + "/seg_join/corpus.txt"
        with open(corpus_name, "r") as corpus:
            self.texts = corpus.readlines()
        sql = "select id, category from %s" % self.project_name
        results = db.execute(sql)
        db.close()
        self.labels = [row[1] for row in results]

        # 添加标题和标签特征
        print "reading title & tags..."
        doc_num = len(self.labels)
        for i in xrange(doc_num):
            tt_name = "%s/tt/%d" % (self.project_name, i + 1)
            with open(tt_name, "r") as tt_file:
                title = tt_file.readline()
                tags = tt_file.readline()
                self.texts[i] += (" " + title) * 5 + (" " + tags) * 3

        # 切分训练数据和测试数据
        x = self.texts
        y = self.labels
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=1)

        # 训练
        print "training..."
        self.pipeline.fit(x_train, y_train)

        # 测试
        print "testing..."
        y_pred = self.pipeline.predict(x_test)
        print(metrics.classification_report(y_test, y_pred))

        # 生成heatmap图
        print "drawing..."
        num = 16
        m = np.zeros([num, num])
        for x, y in zip(y_pred, y_test):
            m[x - 1, y - 1] += 1
        for y in xrange(num):
            total = sum(m[:, y])
            if total > 0:
                m[:, y] /= total
        category = Category()
        label_list = [category.n2c[i + 1] for i in xrange(1, 17)]
        index = pd.Index(label_list, dtype=str)
        df = pd.DataFrame(m, index=index, columns=label_list)
        sns.set(style="white")
        f, ax = plt.subplots(figsize=(11, 9))
        cmap = sns.diverging_palette(220, 10, as_cmap=True)
        sns.heatmap(m, cmap=cmap, vmax=1.0,
                    square=True,
                    linewidths=.5, cbar_kws={"shrink": .5}, ax=ax)
        plt.xticks(rotation=-90)
        plt.yticks(rotation=0)
        f.savefig("tfidf_clf_result.png")

    def predict(self, x):
        return self.pipeline.predict(x)

    def transform(self, x):
        return self.pipeline_transform.transform(x)


class TextClassifierDoc2Vec:
    def __init__(self, project_name):
        self.project_name = project_name
        self.clf = SVC()
        self.model = None

    def train(self):
        # 导入数据
        db = ArticleDB()
        # 训练doc2vec
        print "training dod2vec model..."
        corpus_name = self.project_name + "/seg_join/corpus.txt"
        if not os.path.exists('./news.d2v'):
            self.model = Doc2Vec(min_count=1, window=10, size=400, sample=1e-4, negative=5, workers=8)
            sources = {corpus_name: 'TRAIN'}
            sentences = LabeledLineSentence(sources)
            self.model.build_vocab(sentences.to_array())
            for epoch in range(10):
                self.model.fit(sentences.sentences_perm())
                self.model.save('./news.d2v')
        else:
            self.model = Doc2Vec.load('./news.d2v')

        # 切分训练数据和测试数据
        print "transform docs to vecs..."
        results = db.execute("select id, category from %s" % self.project_name)
        y = [row[1] for row in results]
        results = db.execute("select count(id) from %s" % self.project_name)
        doc_num = results[0][0]
        db.close()
        x = [self.model.docvecs["TRAIN_%d" % i] for i in range(doc_num)]
        Dumper.save(x, "doc_vec_all.dat")
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=1)

        # 训练
        print "training classifier using doc2vec features..."
        self.clf.fit(x_train, y_train)

        # 测试
        print "testing classifier..."
        y_pred = self.clf.predict(x_test)
        print(metrics.classification_report(y_test, y_pred))

        # 生成heatmap图
        num = 16
        m = np.zeros([num, num])
        for x, y in zip(y_pred, y_test):
            m[x - 1, y - 1] += 1
        for y in xrange(num):
            total = sum(m[:, y])
            if total > 0:
                m[:, y] /= total
        label_list = [Category.n2c[i+1] for i in xrange(1, 17)]
        print label_list
        index = pd.Index(label_list, dtype=str)
        df = pd.DataFrame(m, index=index, columns=label_list)
        sns.set(style="white")
        f, ax = plt.subplots(figsize=(11, 9))
        cmap = sns.diverging_palette(220, 10, as_cmap=True)
        sns.heatmap(df, cmap=cmap, vmax=1.0,
                    square=True,
                    linewidths=.5, cbar_kws={"shrink": .5}, ax=ax)
        plt.xticks(rotation=-90)
        plt.yticks(rotation=0)
        f.savefig("doc2vec_clf_result.png")

    def predict(self, x):
        return self.clf.predict(x)

    def transform(self, x):
        if isinstance(x, list):
            return self.model.infer_vector(x)
        else:
            print "ERROR: doc2vec输入必须为词语的list"
            return None


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
                    self.sentences.append(TaggedDocument(utils.to_unicode(line).split(), [unicode(prefix + '_%s' % item_no)]))
        return self.sentences

    def sentences_perm(self):
        shuffle(self.sentences)
        return self.sentences


class TextClassifierCharacter:
    def __init__(self, project_name):
        self.project_name = project_name
        self.clf = SVC(kernel="linear")

    def train(self):
        # 获取文章总数
        db = ArticleDB()
        id_cats = db.execute("select id, category from %s" % self.project_name)
        ids = [row[0] for row in id_cats]
        cats = [row[1] for row in id_cats]
        db.close()
        freq_util = FreqCharUtil()

        # 导入数据
        print "reading corpus.txt ..."
        corpus = []
        mms = [0.0] * freq_util.freq_char_num
        for id, cat in zip(ids, cats):
            txt_name = self.project_name + "/txt/" + str(id)
            with open(txt_name, "r") as txt_file:
                text = txt_file.read()
                vec = freq_util.get_vec(text)
                for i in xrange(freq_util.freq_char_num):
                    mms[i] = max(mms[i], vec[i])
                corpus.append(vec)

        for vec in corpus:
            for i in xrange(freq_util.freq_char_num):
                vec[i] /= mms[i]

        # 切分训练和测试数据
        x = np.asarray(corpus)
        y = np.asarray(cats)
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=1)

        # 训练
        print "training classifier using doc2vec features..."
        self.clf.fit(x_train, y_train)

        # 测试
        print "testing classifier..."
        y_pred = self.clf.predict(x_test)
        print(metrics.classification_report(y_test, y_pred))


    def predict(self, x):
        return self.clf.predict(x)

    def transform(self, x):
        if isinstance(x, list):
            return self.model.infer_vector(x)
        else:
            print "ERROR: doc2vec输入必须为词语的list"
            return None


class TextClassifierSub:
    def __init__(self, project_name):
        self.project_name = project_name
        self.subcat_profile = "subcat"
        self.tfidf = TfidfVectorizer()
        self.clf = SGDClassifier()
        self.pipeline = Pipeline([
            ('tfidf', self.tfidf),
            ('clf', self.clf)])
        self.pipeline_transform = Pipeline([
            ('tfidf', self.tfidf)])

    def train(self):
        # 读取子类分类规格文件
        cat2subcat, tag2id = read_subcat(self.subcat_profile)

        # 标注训练数据
        print "dividing category into sub-categories..."
        db = ArticleDB()
        db.execute("update %s set subcategory=null" % self.project_name)
        db.commit()
        for fcat, subcats in cat2subcat.items():
            ids = db.execute("select id from %s where category=%s" % (self.project_name, fcat))
            ids = [id[0] for id in ids]
            print "\tcategory %d has %d files, divide into %d subcategories" % (fcat, len(ids), len(subcats))
            for id in ids:
                attr_name = "%s/attr/%d" % (self.project_name, id)
                with open(attr_name, "r") as attr_file:
                    tags = attr_file.readlines()[3].strip()
                    if len(tags) > 0:
                        tags = tags.split(" ")
                        subtag2id = tag2id[fcat]
                        for tag in tags:
                            if tag in subtag2id:
                                subcat = subtag2id[tag]
                                db.execute("update %s set subcategory=%d where id=%d" % (self.project_name, subcat, id))
                                break
        db.commit()

        # 训练分类器（对每个类别，利用其子类分类）
        fcats = cat2subcat.keys()
        for fcat in fcats:
            id_subcats = db.execute("select id, subcategory from %s where category=%s and subcategory is not null" % (self.project_name, fcat))
            ids = [row[0] for row in id_subcats]
            y = [row[1] for row in id_subcats]
            x = []
            print "category %d: reading corpus..." % fcat
            for id in ids:
                seg_name = "%s/seg/%d" % (self.project_name, id)
                with open(seg_name, "r") as seg_file:
                    lines = [line.strip() for line in seg_file.readlines() if len(line.strip()) > 0]
                    text = " ".join(lines)
                    x.append(text)

            # 切分训练数据和测试数据
            print "category %d: splitting train and test..." % fcat
            x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=1)

            # 训练
            print "category %d: training..." % fcat
            self.pipeline.fit(x_train, y_train)

            # 测试
            print "category %d: testing..." % fcat
            y_pred = self.pipeline.predict(x_test)
            print(metrics.classification_report(y_test, y_pred))

            # 预测
            test_proj_name = "article150801160830"
            ids = db.execute("select id from %s where category=%d" % (test_proj_name, fcat))
            ids = [row[0] for row in ids]
            print "category %d: predicting new corpus..." % fcat
            for id in ids:
                seg_name = "%s/seg/%d" % (test_proj_name, id)
                with open(seg_name, "r") as seg_file:
                    lines = [line.strip() for line in seg_file.readlines() if len(line.strip()) > 0]
                    text = " ".join(lines)
                    x.append(text)
            y = self.pipeline.predict(x)

            print "category %d: writing predict result to sql..." % fcat
            for id, label in zip(ids, y):
                db.execute("update %s set subcategory=%d where id=%d" % (test_proj_name, label, id))

        db.commit()
        db.close()

        # 全部结束
        print "OK, all done!"

if __name__ == "__main__":

    clf = TextClassifierSub(project_name="article_cat")
    clf.train()

    # clf = TextClassifierSub(project_name="article_cat")
    # clf.train()

    # stopword = StopWord("./stopwords_it.txt")
    # proj_name = "article150801160830"
    # # 载入语料库(from seg_join/corpus.txt)
    # corpus = []
    # print "reading corpus"
    # count = 1
    # with open(proj_name + "/seg_join/corpus.txt", "r") as corpus_file:
    #     for line in corpus_file:
    #         print "read line %d" % count; count += 1
    #         words = line.split()
    #         words = [word for word in words if not stopword.is_stop_word(word)]
    #         corpus.append(words)
    #         # Dumper.save(corpus, corpus_name)
    # doc_num = len(corpus)
    #
    # # 分析每篇文章的doc2vec，并保存磁盘作为特征
    # obj_dir = proj_name + "/clt_doc2vec/"
    # corpus_bow = None
    # corpus_vecs = []
    # for i, doc in enumerate(corpus):
    #     print "doc2vec for doc %d/%d" % (i + 1, doc_num)
    #     topic_weights = clf.transform(doc)
    #     corpus_vecs.append(topic_weights)
    #
    # cluster_num1 = 10
    # cluster_num2 = 5
    # category_offset = 0
    # # 第一次聚类
    # print "first clustering..."
    # corpus_vecs = np.asarray(corpus_vecs)
    # clt = KMeans(n_clusters=cluster_num1)
    # clt.fit(corpus_vecs)
    #
    # # 第一次聚类结果写入mysql
    # print "4. writing clustering result to mysql..."
    # db = ArticleDB()
    # for i in xrange(doc_num):
    #     db.execute("update %s set category1=%d where id=%d" % (proj_name, clt.labels_[i], i + 1))
    # category_offset += cluster_num1
    #
    # # 按照第一次聚类结果，对文章分组
    # clusters = [[] for i in xrange(cluster_num1)]
    # for i in xrange(doc_num):
    #     clusters[clt.labels_[i]].append(i + 1)
    #
    # # 第二次聚类(分组进行)
    # for i in xrange(cluster_num1):
    #     print "second clustering: %d/%d ..." % (i + 1, cluster_num1)
    #     # 第二次聚类
    #     sub_vecs = [corpus_vecs[j - 1] for j in clusters[i]]
    #     clt = KMeans(n_clusters=cluster_num2)
    #     clt.fit(sub_vecs)
    #
    #     # 第二次聚类结果写入mysql
    #     print "writing clustering result to mysql..."
    #     for j in xrange(len(clusters[i])):
    #         db.execute("update %s set category2=%d where id=%d" % (
    #         proj_name, category_offset + clt.labels_[j], clusters[i][j]))
    #
    #     # 类别ID起始编码
    #     category_offset += cluster_num2
    #
    # db.commit()
    # db.close()
    # print "ok, successfully complete!"
