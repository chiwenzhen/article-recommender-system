# coding:utf-8

import os
from gensim import corpora
from gensim.models.ldamodel import LdaModel
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import Normalizer
from sklearn.pipeline import make_pipeline
from collections import defaultdict
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist, squareform
from scipy.cluster.hierarchy import ward, linkage, dendrogram
from myutils import ArticleDB, read_subclt, Dumper, StopWord, ArticleDumper, Category
from treelib import Node, Tree
from sklearn.cluster import KMeans, MiniBatchKMeans
import shutil
import numpy as np
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.pipeline import Pipeline
from sklearn.cross_validation import train_test_split
from sklearn import metrics
from sklearn.metrics import silhouette_samples, silhouette_score


class LDA:
    def __init__(self, proj_name):
        self.proj_name = proj_name
        self.seg_dir = proj_name + "/" + "seg"
        self.attr_dir = proj_name + "/" + "attr"
        self.tag_dict = defaultdict(int)
        self.lda = None
        self.corpus = []
        self.doc_num = None  # doc num in corpus
        self.corpus_bow = None
        self.id2word = None
        self.topic_num = 50
        self.tree = Tree()
        self.tree.create_node("Root", -1)

        self.obj_dir = self.proj_name + "/clt_topic/"
        shutil.rmtree(self.obj_dir, ignore_errors=True)
        os.mkdir(self.obj_dir)

    # 从seg文件夹中载入语料库
    def load_corpus(self, seg_dir):
        corpus = []
        seg_names = [f for f in os.listdir(seg_dir) if os.path.isfile(os.path.join(seg_dir, f))]
        for seg_name in seg_names:
            with open(os.path.join(seg_dir, seg_name), 'r') as seg_file:
                doc = []
                for sentence in seg_file:
                    sentence = sentence.strip()  # 删除前后空格，换行等空白字符
                    sentence = sentence.decode("utf-8")  # utf-8转unicode
                    words = sentence.split(u" ")
                    words = [word.strip() for word in words if len(word.strip()) > 0]
                    doc.extend(words)
                corpus.append(doc)
        return corpus

    def fit(self):
        # 载入IT停用词
        stopword = StopWord("./stopwords_it.txt")

        # 载入语料库(from seg_join/corpus.txt)
        print "reading corpus"
        corpus_name = "corpus.dat"
        if not os.path.exists(corpus_name):
            with open(self.proj_name + "/seg_join/corpus.txt", "r") as corpus_file:
                for line in corpus_file:
                    words = line.split()
                    words = [word for word in words if not stopword.is_stop_word(word)]
                    self.corpus.append(words)
            # Dumper.save(self.corpus, corpus_name)
        else:
            self.corpus = Dumper.load(corpus_name)
        self.doc_num = len(self.corpus)

        # 生成文档的词典，每个词与一个整型索引值对应
        print "creating dictionary"
        id2word_name = "id2word.dat"
        if not os.path.exists(id2word_name):
            self.id2word = corpora.Dictionary(self.corpus)
            # Dumper.save(self.id2word, id2word_name)
        else:
            self.id2word = Dumper.load(id2word_name)

        # 删除低频词
        # ignore words that appear in less than 20 documents or more than 10% documents
        # id2word.filter_extremes(no_below=20, no_above=0.1)

        # 词频统计，转化成空间向量格式
        print "tranforming doc to vector"
        corpus_bow_name = "corpus_bow.dat"
        if not os.path.exists(corpus_bow_name):
            self.corpus_bow = [self.id2word.doc2bow(doc) for doc in self.corpus]
            # Dumper.save(self.corpus_bow, corpus_bow_name)
        else:
            self.corpus_bow = Dumper.load(corpus_bow_name)

        # 训练LDA模型
        print "training lda model"
        lda_model_name = "lda_models/lda.dat"
        if not os.path.exists(lda_model_name):
            lda = LdaModel(corpus=self.corpus_bow, id2word=self.id2word, num_topics=self.topic_num, alpha='auto')
            Dumper.save(lda, lda_model_name)
        else:
            lda = Dumper.load(lda_model_name)

        # 打印识别出的主题
        topics = lda.print_topics(num_topics=self.topic_num, num_words=10)
        for topic in topics:
            print "topic %d: %s" % (topic[0], topic[1].encode("utf-8"))
        with open("topics.txt", "w") as topic_file:
            for topic in topics:
                print >> topic_file, "topic %d: %s" % (topic[0], topic[1].encode("utf-8"))
        self.lda = lda

    def tranform(self):
        # 分析每篇文章的主题分布，并保存磁盘作为特征
        corpus_vecs = []
        for i, doc_bow in enumerate(self.corpus_bow):
            print "infer topic vec: %d/%d" % (i+1, self.doc_num)
            topic_id_weights = self.lda.get_document_topics(doc_bow, minimum_probability=-1.0)
            topic_weights = [item[1] for item in topic_id_weights]
            corpus_vecs.append(topic_weights)
            obj_name = self.obj_dir + str(i + 1)
            Dumper.save(topic_weights, obj_name)

        cluster_num1 = 10
        cluster_num2 = 5
        category_offset = 0
        # 第一次聚类
        print "first clustering..."
        corpus_vecs = np.asarray(corpus_vecs)
        clt = KMeans(n_clusters=cluster_num1)
        clt.fit(corpus_vecs)

        # 第一次聚类结果写入mysql
        print "writing clustering result to mysql..."
        db = ArticleDB()
        for i in xrange(self.doc_num):
            db.execute("update %s set category1=%d where id=%d" % (self.proj_name, clt.labels_[i], i + 1))
        category_offset += cluster_num1

        # 按照第一次聚类结果，对文章分组
        clusters = [[] for i in xrange(cluster_num1)]
        for i in xrange(self.doc_num):
            clusters[clt.labels_[i]].append(i + 1)

        # 第二次聚类(分组进行)
        for i in xrange(cluster_num1):
            print "second clustering: %d/%d ..." %(i+1, cluster_num1)
            # 第二次聚类
            sub_vecs = [corpus_vecs[j - 1] for j in clusters[i]]
            clt = KMeans(n_clusters=cluster_num2)
            clt.fit(sub_vecs)

            # 第二次聚类结果写入mysql
            print "writing clustering result to mysql..."
            for j in xrange(len(clusters[i])):
                db.execute("update %s set category2=%d where id=%d" % (self.proj_name, category_offset + clt.labels_[j], clusters[i][j]))

            # 类别ID起始编码
            category_offset += cluster_num2

        db.commit()
        db.close()
        print "ok, successfully complete!"

    def predict(self, x):
            # update the LDA model with additional documents
            self.lda.update(x)
            return None

    # 统计每个标签出现的次数
    def count_tag(self, attr_dir):
        attr_names = [f for f in os.listdir(attr_dir) if os.path.isfile(os.path.join(attr_dir, f))]
        for attr_name in attr_names:
            with open(os.path.join(attr_dir, attr_name), 'r') as seg_file:
                sentences = seg_file.readlines()
                if len(sentences) > 3:
                    tags = sentences[3].strip()
                    tags = tags.split(" ")
                    for tag in tags:
                            self.tag_dict[tag] += 1
        self.tag_dict = sorted(self.tag_dict.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
        with open("tags.txt", "w") as seg_file:
            for key, value in self.tag_dict:
                print >> seg_file, "%s : %d" % (key, value)


class TextClusteringSub:
    def __init__(self, proj_name):
        self.proj_name = proj_name
        self.subcat_profile = "subcat"
        self.tfidf = TfidfVectorizer()
        self.ch2 = SelectKBest(chi2, k=20)

    def train(self):
        db = ArticleDB()
        db.execute("update %s set subcluster=null" % self.proj_name)
        db.commit()
        # 聚类（for 每个类别）
        subclt_offset, cat2subclt = read_subclt("subclt")
        for fcat in subclt_offset.keys():
            ids = db.execute("select id from %s where category=%s" % (self.proj_name, fcat))
            ids = [row[0] for row in ids]
            if len(ids) < 10:
                continue

            # 读取文本
            print "category %d: reading corpus..." % fcat
            x = []
            for id in ids:
                seg_name = "%s/seg/%d" % (self.proj_name, id)
                with open(seg_name, "r") as seg_file:
                    lines = [line.strip() for line in seg_file.readlines() if len(line.strip()) > 0]
                    text = " ".join(lines)
                    x.append(text)

            # tfidf计算
            print "category %d: calc tfidf..." % fcat
            vectorizer = TfidfVectorizer()
            x = vectorizer.fit_transform(x)

            # 降维
            # print "category %d: decomposition..." % fcat
            # svd = TruncatedSVD(1000)
            # normalizer = Normalizer(copy=False)
            # lsa = make_pipeline(svd, normalizer)
            # x = lsa.fit_transform(x)

            # 选择合适的k
            # range_n_clusters = [4, 6, 8, 10, 12, 14, 16]
            # silhouette_avgs = []
            # for n_clusters in range_n_clusters:
            #     clusterer = KMeans(n_clusters=n_clusters, random_state=10)
            #     cluster_labels = clusterer.fit_predict(x)
            #     silhouette_avg = silhouette_score(x, cluster_labels)
            #     print("For n_clusters =", n_clusters, "The average silhouette_score is :", silhouette_avg)
            #     silhouette_avgs.append(silhouette_avg)
            # max_idx = np.argmax(silhouette_avgs)
            # cluster_num = range_n_clusters[max_idx]

            # 训练
            subcats = cat2subclt[fcat]
            cluster_num = len(subcats)
            print "category %d: clustering (n_cluster=%d)..." % (fcat, cluster_num)
            # cluster_num = len(cat2subclt[fcat])
            clt = KMeans(n_clusters=cluster_num)
            clt.fit(x)

            # 写回SQL
            print "category %d: writing cluster result to sql..." % fcat
            offset = subclt_offset[fcat]
            for i, id in enumerate(ids):
                db.execute("update %s set subcluster=%d where id=%d" % (self.proj_name, offset + clt.labels_[i], id))

            # 寻找分类关键词
            # feature_names = vectorizer.get_feature_names()
            # y = clt.labels_
            # ch2 = SelectKBest(chi2, k=20)
            # x = ch2.fit(x, y)
            # key_words = [feature_names[i] for i in ch2.get_support(indices=True)]
            # key_words = " ".join(key_words)
            # print "关键词："
            # print key_words

            # 寻找簇的名称
            print "category %d: reading corpus..." % fcat
            x = []
            for id in ids:
                seg_name = "%s/seg/%d" % (self.proj_name, id)
                with open(seg_name, "r") as seg_file:
                    lines = [line.strip() for line in seg_file.readlines() if len(line.strip()) > 0]
                    text = " ".join(lines)
                    x.append(text)
            text_group = [""] * cluster_num
            doc_num = len(ids)
            for i in xrange(doc_num):
                text_group[clt.labels_[i]] += x[i]

            vectorizer = TfidfVectorizer()
            matrix = vectorizer.fit_transform(text_group)
            feature_names = vectorizer.get_feature_names()
            for i in xrange(cluster_num):
                row = matrix[i].toarray().flatten()
                idxs = np.argsort(row)
                idxs = idxs[::-1]
                idxs = idxs[:20]
                keywords = [feature_names[j] for j in idxs]
                keywords = " ".join(keywords)
                print "subcluster-", offset+i, subcats[i].name, ":\t", keywords

        db.commit()
        db.close()

        # 全部结束
        print "OK, all done!"


# 为每个一级分类做LDA，每个一级类生成5个二级主题，结果不怎么好
class TextClusteringSubLDA:
    def __init__(self, proj_name):
        self.proj_name = proj_name
        self.subcat_profile = "subcat"
        self.tfidf = TfidfVectorizer()
        self.ch2 = SelectKBest(chi2, k=1000)

    def train(self):
        db = ArticleDB()
        category = Category()
        db.execute("update %s set subcluster=null" % self.proj_name)
        db.commit()
        # 聚类（for 每个类别）
        subclt_offset, cat2subclt = read_subclt("subclt")
        for fcat in subclt_offset.keys():
            ids = db.execute("select id from %s where category=%s" % (self.proj_name, fcat))
            ids = [row[0] for row in ids]
            if len(ids) < 10:
                continue

            # 读取文本
            print "category %d: reading corpus..." % fcat
            x = []
            for id in ids:
                seg_name = "%s/seg/%d" % (self.proj_name, id)
                with open(seg_name, "r") as seg_file:
                    lines = [line.strip() for line in seg_file.readlines() if len(line.strip()) > 0]
                    text = " ".join(lines)
                    text = text.split()
                    x.append(text)

            # dict
            print "category %d: dictionary..." % fcat
            id2word = corpora.Dictionary(x)
            # bow
            print "category %d: bag of word..." % fcat
            corpus_bow = [id2word.doc2bow(doc) for doc in x]
            # lda
            print "category %d: lda modeling..." % fcat
            lda = LdaModel(corpus=corpus_bow, id2word=id2word, num_topics=5, alpha='auto')
            # show topics
            print "category %d: 【%s】show topics..." % (fcat, category.n2c[fcat])
            topics = lda.print_topics(num_topics=-1, num_words=10)
            for topic in topics:
                print "topic %d: %s" % (topic[0], topic[1].encode("utf-8"))

            # 写回SQL
            # print "category %d: writing cluster result to sql..." % fcat
            # offset = subclt_offset[fcat]
            # for i, id in enumerate(ids):
            #     db.execute("update %s set subcluster=%d where id=%d" % (self.proj_name, offset + clt.labels_[i], id))
        db.commit()
        db.close()

        # 全部结束
        print "OK, all done!"

if __name__ == '__main__':
    # lda_model = LDA(proj_name="article150801160830")
    # lda_model.fit()
    # lda_model.tranform()
    clt = TextClusteringSub(proj_name="article150801160830")
    clt.train()
