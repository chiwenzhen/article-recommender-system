# coding:utf-8

import os
from gensim import corpora
from gensim.models.ldamodel import LdaModel
from collections import defaultdict
from myutils import ArticleDB, Dumper, StopWord, ArticleDumper
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist, squareform
from scipy.cluster.hierarchy import ward, linkage, dendrogram
from myutils import ArticleDB
from treelib import Node, Tree


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
        self.topic_num = 10
        self.sub_topic_num = 5
        self.tree = Tree()
        self.tree.create_node("Root", -1)

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
        print "creating di dictionary"
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

        # 给每个主题起名字
        topics = lda.show_topics(num_topics=self.topic_num, num_words=2, log=False, formatted=False)
        topic_names = [topic[1][0][0] + "+" + topic[1][1][0] for topic in topics]
        for i, topic_name in enumerate(topic_names):
            self.tree.create_node((i, topic_name), i, parent=-1)

        # 打印识别出的主题
        topics = lda.print_topics(num_topics=self.topic_num, num_words=10)
        for topic in topics:
            print "topic %d: %s" % (topic[0], topic[1].encode("utf-8"))
        with open("topics.txt", "w") as topic_file:
            for topic in topics:
                print >> topic_file, "topic %d: %s" % (topic[0], topic[1].encode("utf-8"))
        self.lda = lda

    def tranform(self):
        # 分析每篇文章的主题
        db = ArticleDB()
        topic_doc_ids = [[] for i in xrange(self.topic_num)]
        topic_docs = [[] for i in xrange(self.topic_num)]
        for i, doc_bow in enumerate(self.corpus_bow):
            doc_topics = self.lda[doc_bow]
            if len(doc_topics) == 0:
                print "no topics for doc %d " % i+1
                continue
            topic_item = max(doc_topics, key=lambda topic_item: topic_item[1])
            topic_id = topic_item[0]
            topic_doc_ids[topic_id].append(i + 1)
            topic_docs[topic_id].append(self.corpus[i])
            db.execute("update %s set lda_category1=%d where id = %d" % (self.proj_name, topic_id, i + 1))
        db.commit()
        db.close()

        # 对分组内文章再次进行主题分析
        topic_offset = self.topic_num
        for topic_fid in xrange(self.topic_num):
            sub_ids = topic_doc_ids[topic_fid]
            sub_corpus = topic_docs[topic_fid]

            # 生成字典
            print "creating di dictionary"
            sub_id2word = corpora.Dictionary(sub_corpus)

            # 删除低频词
            # ignore words that appear in less than 20 documents or more than 10% documents
            # id2word.filter_extremes(no_below=20, no_above=0.1)

            # 词频统计，转化成空间向量格式
            print "tranforming doc to vector"
            sub_corpus_bow = [sub_id2word.doc2bow(doc_bow) for doc_bow in sub_corpus]

            # 训练LDA模型
            print "training lda model"
            sub_lda_model_name = "lda_models/lda_%d.dat" % topic_fid
            if not os.path.exists(sub_lda_model_name):
                sub_lda = LdaModel(corpus=sub_corpus_bow, id2word=sub_id2word, num_topics=self.sub_topic_num, alpha='auto')
                Dumper.save(sub_lda, sub_lda_model_name)
            else:
                sub_lda = Dumper.load(sub_lda_model_name)

            # 给每个主题起名字
            sub_topics = sub_lda.show_topics(num_topics=self.sub_topic_num, num_words=2, log=False, formatted=False)
            sub_topic_names = [sub_topic[1][0][0] + "+" + sub_topic[1][1][0] for sub_topic in sub_topics]
            for i, sub_topic_name in enumerate(sub_topic_names):
                self.tree.create_node((topic_offset+i, sub_topic_name), topic_offset+i, parent=topic_fid)

            # 打印识别出的主题
            sub_topics = sub_lda.print_topics(num_topics=self.sub_topic_num, num_words=10)
            for sub_topic in sub_topics:
                print "sub topic %d: %s" % (sub_topic[0], sub_topic[1].encode("utf-8"))
            with open("sub_topics_%d.txt" % topic_fid, "w") as topic_file:
                for sub_topic in sub_topics:
                    print >> topic_file, "topic %d: %s" % (sub_topic[0], sub_topic[1].encode("utf-8"))

            # 分析每篇文章的主题
            db = ArticleDB()
            for i, doc_bow in enumerate(sub_corpus_bow):
                doc_topics = sub_lda[doc_bow]
                if len(doc_topics) == 0:
                    print "no sub topics for doc %d " % sub_ids[i]
                    continue
                topic_item = max(doc_topics, key=lambda topic_item: topic_item[1])
                topic_id = topic_item[0]
                db.execute("update %s set lda_category2=%d where id = %d" % (self.proj_name, topic_offset + topic_id, sub_ids[i]))
            db.commit()
            db.close()
            topic_offset += self.sub_topic_num

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


class HierarchicalClustering:
    def __init__(self):
        pass

if __name__ == '__main__':
    lda_model = LDA(proj_name="article150801160830")
    lda_model.fit()
    lda_model.tranform()
