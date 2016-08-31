# coding:utf-8

import os
from gensim import corpora, models
from collections import defaultdict
from myutils import ArticleDB, Dumper

class LDAWordFilter:
    pass


class LDA:
    def __init__(self, proj_name):
        self.proj_name = proj_name
        self.seg_dir = proj_name + "/" + "seg"
        self.attr_dir = proj_name + "/" + "attr"
        self.tag_dict = defaultdict(int)

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

    def train(self):
        if not os.path.exists("./lda.model"):
            # 载入语料库(from seg_join/corpus.txt)
            print "read corpus"
            corpus = []
            with open(self.proj_name + "/seg_join/corpus.txt", "r") as corpus_file:
                for line in corpus_file:
                    words = line.split()
                    corpus.append(words)


            # 生成文档的词典，每个词与一个整型索引值对应
            print "word->id"
            word_dict = corpora.Dictionary(corpus)


            # 词频统计，转化成空间向量格式
            corpus = [word_dict.doc2bow(doc) for doc in corpus]
            print "doc->bow"

            # 训练LDA模型
            print "bow->lda"
            lda = models.ldamodel.LdaModel(corpus=corpus, id2word=word_dict, num_topics=30, alpha='auto')
            Dumper.dump(lda, "./lda.model")
        else:
            lda = Dumper.load("./lda.model")

        # 打印识别出的主题
        topics = lda.print_topics(num_topics=15, num_words=30)
        for topic in topics:
            print "topic %d: %s" % (topic[0], topic[1].encode("utf-8"))
        with open("topics.txt", "w") as topic_file:
            for topic in topics:
                print >> topic_file, "topic %d: %s" % (topic[0], topic[1].encode("utf-8"))
        return lda

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

if __name__ == '__main__':
    LDA(proj_name="article150801160830").train()