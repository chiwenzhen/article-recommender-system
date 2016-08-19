# coding=utf-8
import thulac
import os
import os.path
import MySQLdb


class Segmenter:
    def __init__(self):
        # 创建分词文件存放目录
        if not os.path.exists("articles/seg/"):
            os.makedirs("articles/seg/")

        # 分句符号
        delimiters = u"\u00a0＃[。，,！……!《》<>\"':：？\?、\|“”‘’；]{}（）{}【】()｛｝（）：？！。，;、~——+％%`:“”＂'‘\n\r"
        self.delimiters = set(delimiters)

        # 连接数据库，获取文章总数
        self.db = MySQLdb.connect(host="localhost", user="root", passwd="123456", db="test", charset='utf8')
        try:
            cursor = self.db.cursor()
            sql = "select count(*) from article"
            cursor.execute(sql)
            results = cursor.fetchall()
            self.doc_count = results[0][0]
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])

        # 分词工具初始化
        self.thu_seg = thulac.thulac("-seg_only -model_dir models/")

    # 分词
    def seg(self):
        # 遍历所有文件，查找.word文件是否存在，不存在则进行分词
        for i in range(1, self.doc_count + 1):
            doc_txt_name = "articles/txt/%d" % i
            doc_seg_tmp = "articles/seg/%d.tmp" % i
            doc_seg_name = "articles/seg/%d" % i
            if not os.path.exists(doc_seg_name):  # 如果分词文件不存在，那么进行分词
                doc_words = []
                file_txt = open(doc_txt_name, "r")
                file_tmp = open(doc_seg_tmp, "w")
                for line in file_txt.readlines():
                    sentences = self.seg_sentence(line)
                    for sentence in sentences:
                        doc_words.append(" ".join(self.thu_seg.cut(sentence)) + "\n")
                file_tmp.writelines(doc_words)
                file_txt.close()
                file_tmp.close()
                os.rename(doc_seg_tmp, doc_seg_name)

    # 分句
    def seg_sentence(self, line):
        sentences = []  # 句子列表
        sentence = []  # 句子
        line = line.strip()
        line += "。"  # 最后添加句号
        line = line.decode("utf-8")
        for c in line:
            if c in self.delimiters:  # 如果当前字符是分句符号
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
    seg = Segmenter()
    seg.seg()
