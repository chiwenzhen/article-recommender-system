# coding:utf-8

import os
from gensim import corpora, models
from collections import defaultdict


class ArticleClustering:
    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.seg_dir = root_dir + "/" + "seg"
        self.attr_dir = root_dir + "/" + "attr"
        self.tag_dict = defaultdict(int)
        pass
        pass

    def clustering(self):
        self.count_tag(self.attr_dir)
        # words_list = self.get_words_list(self.seg_dir)
        # self.model_lda(words_list)

    @staticmethod
    def get_words_list(seg_dir):
        texts = []
        seg_names = [f for f in os.listdir(seg_dir) if os.path.isfile(os.path.join(seg_dir, f))]
        for seg_name in seg_names:
            with open(os.path.join(seg_dir, seg_name), 'r') as seg_file:
                text = []
                for sentence in seg_file:
                    sentence = sentence.strip()  # 删除前后空格，换行等空白字符
                    sentence = sentence.decode("utf-8")  # utf-8转unicode
                    words = sentence.split(u" ")
                    words = [word.strip() for word in words if len(word.strip()) > 0]
                    text.extend(words)
                texts.append(text)
        return texts

    @staticmethod
    def model_lda(words_list):
        # 生成文档的词典，每个词与一个整型索引值对应
        word_dict = corpora.Dictionary(words_list)
        print "words->id"
        # 词频统计，转化成空间向量格式
        corpus_list = [word_dict.doc2bow(text) for text in words_list]
        print "words->vector"

        lda = models.ldamodel.LdaModel(corpus=corpus_list, id2word=word_dict, num_topics=30, alpha='auto')
        print "lda model complete"

        topics = lda.print_topics(30)
        for topic in topics:
            print "topic %d: %s" % (topic[0], topic[1].encode("utf-8"))

        with open("topics.txt", "w") as topic_file:
            for topic in topics:
                print >> topic_file, "topic %d: %s" % (topic[0], topic[1].encode("utf-8"))
        return lda

    # 统计每个标签出现的次数
    def count_tag(self, attr_dir):
        attr_names = [f for f in os.listdir(attr_dir) if os.path.isfile(os.path.join(attr_dir, f))]
        attr_name_num = len(attr_names)
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
    # 获取分词和过滤无用词后的词语序列列表
    ArticleClustering("articles").clustering()
