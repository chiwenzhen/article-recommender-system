# coding:utf-8

import os
from gensim import corpora, models


class ArticleClustering:
    def __init__(self, dir):
        words_list = self.get_words_list(dir)
        lda = self.model_lda(words_list)

    def model_lda(self, words_list):
        # 生成文档的词典，每个词与一个整型索引值对应
        word_dict = corpora.Dictionary(words_list)
        # 词频统计，转化成空间向量格式
        corpus_list = [word_dict.doc2bow(text) for text in words_list]
        lda = models.ldamodel.LdaModel(corpus=corpus_list, id2word=word_dict, num_topics=30, alpha='auto')

        output_file = './lda_output.txt'
        with open(output_file, 'w') as f:
            for topic in lda.show_topics():
                print "topic %d: %s" % (topic[0], topic[1].encode("utf-8"))
        return lda

    def get_words_list(self, dir):
        texts = []
        seg_files = [os.path.join(dir, f) for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
        for seg_file in seg_files:
            with open(seg_file, 'r') as file:
                text = []
                for sentence in file:
                    sentence = sentence.strip()  # 删除前后空格，换行等空白字符
                    sentence = sentence.decode("utf-8")  # utf-8转unicode
                    words = sentence.split(u" ")
                    text.extend(words)
                texts.append(text)
        return texts

if __name__ == '__main__':
    # 获取分词和过滤无用词后的词语序列列表
    ArticleClustering("articles/seg/")


