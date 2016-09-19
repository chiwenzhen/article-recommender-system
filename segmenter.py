# coding=utf-8
import thulac
import os
import os.path
import MySQLdb
import shutil
import jieba
import jieba.posseg as pseg
from myutils import StopWord, StopSent, ArticleDB, PosFilter


class Segmenter:
    def __init__(self, proj_name, rm_exist=False):
        # 创建分词文件存放目录，已存在则删除重建
        self.proj_name = proj_name
        self.seg_dir = proj_name + "/seg"
        self.seg_join_dir = proj_name + "/seg_join"
        self.tt_dir = proj_name + "/tt"  # title和tags的分词
        self.pos_seg_dir = proj_name + "/pos_seg"
        if rm_exist:
            shutil.rmtree(self.seg_dir, ignore_errors=True)
            shutil.rmtree(self.seg_join_dir, ignore_errors=True)
            shutil.rmtree(self.tt_dir, ignore_errors=True)
            shutil.rmtree(self.pos_seg_dir, ignore_errors=True)

        try:
            os.makedirs(self.seg_dir)
            os.makedirs(self.seg_join_dir)
            os.makedirs(self.tt_dir)
            os.makedirs(self.pos_seg_dir)
        except:
            pass

        # 分句符号
        self.stop_sent = StopSent()

        # 停用词
        self.stop_word = StopWord("./stopwords_general.txt")

        # 词性过滤
        self.pos_filter = PosFilter()

        # 连接数据库，获取文章总数
        db = ArticleDB()
        try:
            sql = "select count(*) from %s" % proj_name
            self.doc_count = db.execute(sql)[0][0]
            db.close()
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])

    # 分词
    def seg(self, skip_exist=False):
        # self.segtool = thulac.thulac("-seg_only -model_dir models/")
        segtool = jieba
        # 遍历所有文件，进行分词
        for i in range(1, self.doc_count + 1):
            print ("\r%d/%d" % (i, self.doc_count))
            txt_name = "%s/txt/%d" % (self.proj_name, i)
            tmp_name = "%s/seg/%d.tmp" % (self.proj_name, i)
            seg_name = "%s/seg/%d" % (self.proj_name, i)
            doc = []
            if skip_exist and os.path.exists(seg_name):
                continue
            with open(txt_name, "r") as txt_file, open(tmp_name, "w") as tmp_file:
                for line in txt_file.readlines():
                    sentences = self.seg_sentence(line)
                    for sentence in sentences:
                        words = segtool.cut(sentence)
                        words = [word.encode("utf-8") for word in words]  # jieba need, thulac skip this code
                        words = [word for word in words if not self.stop_word.is_stop_word(word)]
                        doc.append(" ".join(words) + "\n")
                tmp_file.writelines(doc)
            os.rename(tmp_name, seg_name)

    # 分词(带词性过滤)
    def pos_seg(self):
        segtool = pseg
        # 遍历所有文件，进行分词
        for i in range(1, self.doc_count + 1):
            print ("\r%d/%d" % (i, self.doc_count))
            txt_name = "%s/txt/%d" % (self.proj_name, i)
            tmp_name = "%s/pos_seg/%d.tmp" % (self.proj_name, i)
            seg_name = "%s/pos_seg/%d" % (self.proj_name, i)
            doc = []
            with open(txt_name, "r") as txt_file, open(tmp_name, "w") as tmp_file:
                for line in txt_file.readlines():
                    sentences = self.seg_sentence(line)
                    for sentence in sentences:
                        words = segtool.cut(sentence)
                        # jieba need the next line code, thulac skip this
                        words = [(word.word.encode("utf-8"), word.flag.encode("utf-8")) for word in words]
                        words = [word for word in words if not self.stop_word.is_stop_word(word[0])]
                        words = [word for word in words if self.pos_filter.is_good_pos(word[1][0])]
                        words = [word[0] for word in words]
                        doc.append(" ".join(words) + "\n")
                tmp_file.writelines(doc)
            os.rename(tmp_name, seg_name)

    # 对标题和标签分词
    def seg_title_tags(self):
        # 遍历所有文件，进行分词
        for i in range(1, self.doc_count + 1):
            print ("\r%d/%d" % (i, self.doc_count))
            txt_name = "%s/txt/%d" % (self.proj_name, i)
            tmp_name = "%s/tt/%d.tmp" % (self.proj_name, i)
            seg_name = "%s/tt/%d" % (self.proj_name, i)
            doc = []
            with open(txt_name, "r") as txt_file, open(tmp_name, "w") as tmp_file:
                lines = [txt_file.readline(), txt_file.readline()]
                for sentence in lines:
                    words = self.segtool.cut(sentence)
                    words = [word.encode("utf-8") for word in words]  # jieba need, thulac skip this code
                    words = [word for word in words if not self.stop_word.is_stop_word(word)]
                    doc.append(" ".join(words) + "\n")
                tmp_file.writelines(doc)
            os.rename(tmp_name, seg_name)

    # 将分词后的每个小文件代表一个文档，将这些文件拼接成一个大文件，大文件每行代表一个文档
    def join_seg_file(self):
        corpus = []
        for i in range(1, self.doc_count + 1):
            seg_name = "%s/%d" % (self.seg_dir, i)
            with open(seg_name, "r") as seg_file:
                lines = [line.strip() for line in seg_file.readlines() if len(line.strip()) > 0]
                doc = " ".join(lines)
                corpus.append(doc)

        corpus = "\n".join(corpus)
        with open(self.seg_join_dir+"/corpus.txt", "w") as seg_join_file:
            seg_join_file.write(corpus)

    # 将分词后的每个小文件代表一个文档，将这些文件拼接成一个大文件，大文件每行代表一个文档
    def join_pos_seg_file(self):
        corpus = []
        for i in range(1, self.doc_count + 1):
            seg_name = "%s/pos_seg/%d" % (self.proj_name, i)
            with open(seg_name, "r") as seg_file:
                lines = [line.strip() for line in seg_file.readlines() if len(line.strip()) > 0]
                doc = " ".join(lines)
                corpus.append(doc)

        corpus = "\n".join(corpus)
        with open(self.seg_join_dir + "/corpus1.txt", "w") as seg_join_file:
            seg_join_file.write(corpus)

    # 分句
    def seg_sentence(self, line):
        sentences = []  # 句子列表
        sentence = []  # 句子
        line = line.strip()
        line += "。"  # 最后添加句号
        line = line.decode("utf-8")
        for c in line:
            if self.stop_sent.is_delim(c):  # 如果当前字符是分句符号
                if len(sentence) == 0:
                    continue
                else:
                    sentence.append(c)  # 将此字符加到句子末尾
                    sentences.append(''.join(sentence).encode("utf-8"))  # 将识别出的句子加入到句子列表中
                    sentence = []  # 句子识别结束，清空开始识别下一句
            else:  # 如果当前字符不是分句符号，则将该字符加到句子末尾
                sentence.append(c)
        return sentences

if __name__ == "__main__":
    segmenter = Segmenter("article_cat")
    # segmenter.seg_title_tags()
    # segmenter.pos_seg()
    # segmenter.join_pos_seg_file()
    segmenter.seg(skip_exist=True)
    segmenter.join_seg_file()

