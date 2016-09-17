# coding=utf-8
import re
from myutils import TopkHeap
import time
import numpy as np
from collections import defaultdict
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from string import letters
from treelib import Node, Tree
import os
from myutils import ArticleDB
import shutil
import json

# here is ubuntu

def add_n_to_file():
    file_num = 19178
    for i in range(1, file_num):
        num = [0, 0, 0, 0]
        with open("article15081608/attr/" + str(i), "r") as file_input:
            lines = file_input.readlines()
            line_num = len(lines)
            if 0 < line_num < 5:
                num[line_num - 1] += 1
            else:
                print "article15081608/attr/" + str(i) + ": " + str(line_num) + "行"
    print "一行：" + str(num[0])
    print "二行：" + str(num[1])
    print "三行：" + str(num[2])
    print "四行：" + str(num[3])

        # with open("article15081608/attr/" + str(i), "a") as file_output:
        #     file_output.write("\n")
        # with open("article15081608/attr/" + str(i), "r") as file_input:
        #     lines = file_input.readlines()
        #     line_num = len(lines)
        #     if 0 < line_num < 5:
        #         num[line_num - 1] += 1
        #     else:
        #         print "article15081608/attr/" + str(i) + ": " + str(line_num) + "行"
        # print "一行：" + str(num[0])
        # print "二行：" + str(num[1])
        # print "三行：" + str(num[2])
        # print "四行：" + str(num[3])

def norm_html():
    with open("tomjerry.html", "r") as file:
        html = file.read()
        # html = "\"tomjerry/bootstrap.min.css\""

        stan = "\"{{ url_for('static', filename='myresources1/bootstrap.min.css') }}\""
        new_html = re.sub(r"\"tomjerry/(.*?)\"",
                          "\"{{ url_for('static', filename='myresources1/\g<1>') }}\"", html)

        print stan == new_html
        print stan
        print new_html

        with open("tomjerry_new.html", "w") as fileo:
            fileo.write(new_html)

def read_file_test():
    with open("a.txt", "r") as file:
        print file.readline()
        print file.readline()

        for line in file.readlines():
            print line

def split_corpus():
    corpus_name = "article15081608" + "/seg_join/corpus.txt"
    corpus_train_name = "article15081608" + "/seg_join/corpus_train.txt"
    corpus_test_name = "article15081608" + "/seg_join/corpus_test.txt"
    with open(corpus_name, "r") as corpus_file:
        pass

def set_test():
    stopword = set([u"直播", u"VR", u"人工智能"])
    print u"直播" in stopword
    print u"VR" in stopword


def tree():
    # 创建类别标签
    cat_tree = Tree()
    cat_tree.create_node((-1, "root"), -1)
    for i in range(10):
        cat_tree.create_node((i, str(i)), i, parent=-1)
    offset = 10
    for i in range(10):
        for j in range(5):
            cur = offset + j
            cat_tree.create_node((cur, str(cur)), cur, parent=i)
        offset += 5

    header1_list = [node.tag for node in cat_tree.children(-1)]
    header2_list = []
    for cat1 in header1_list:
        children = cat_tree.children(cat1[0])
        header2_list.append([node.tag for node in children])

def heat_map():
    y_test=[1,2,1,3,3,5,5,6]
    y_pred=[1,1,1,3,3,4,5,6]
    num = 6
    m = np.zeros([num, num])
    for x, y in zip(y_pred, y_test):
        m[x - 1, y - 1] += 1
    for y in xrange(num):
        total = sum(m[:, y])
        if total > 0:
            m[:, y] /= total

    index = pd.Index(['人工', '金融', '汽车', '教育','手机', '硬件'], dtype=str)
    df = pd.DataFrame(m, index=index, columns=['人工', '金融', '汽车', '教育','手机', '硬件'])

    sns.set(style="white")
    # Set up the matplotlib figure
    f, ax = plt.subplots(figsize=(11, 9))

    # Generate a custom diverging colormap
    cmap = sns.diverging_palette(220, 10, as_cmap=True)

    # Draw the heatmap with the mask and correct aspect ratio
    sns.heatmap(m, cmap=cmap, vmax=1.0,
                square=True, xticklabels=5, yticklabels=5,
                linewidths=.5, cbar_kws={"shrink": .5}, ax=ax)
    f.savefig("output.png")


# 词性过滤
class PosFilter:
    def __init__(self):
        self.pos = set("van")

    # 是否是分句符号 c为uicode编码，非utf-8、ascii等
    def is_good_pos(self, c):
        return c in self.pos


def generate_train_test_small():
    proj_name = "article_cat"
    db = ArticleDB()

    results = db.execute("select distinct category from article_cat")
    categories = [row[0] for row in results]
    sorted(categories)

    train_ids = []
    test_ids = []

    for cat in categories:
        results = db.execute("select id, category from article_cat where category=%d limit 0,150" % cat)
        for item, row in enumerate(results):
            if item < 100:
                train_ids.append((row[0], row[1]))
            else:
                test_ids.append((row[0], row[1]))
    db.close()

    max_len = 0
    with open("%s/seg_join/corpus.txt" % proj_name, "r") as corpus_file, \
            open("%s/seg_join/text_train.csv" % proj_name, "w") as train_file, \
            open("%s/seg_join/text_test.csv" % proj_name, "w") as test_file:
        corpus = corpus_file.readlines()
        train_sentences = ['%d,%d,"%s"\n' % (cat, id, corpus[id-1].strip()) for id, cat in train_ids]
        test_sentences = ['%d,%d,"%s"\n' % (cat, id, corpus[id-1].strip()) for id, cat in test_ids]
        train_file.writelines(train_sentences)
        test_file.writelines(test_sentences)

        for sen in train_sentences:
            cur_len = len(sen.split())
            if  cur_len > max_len:
                max_len = cur_len
        for sen in test_sentences:
            cur_len = len(sen.split())
            if  cur_len > max_len:
                max_len = cur_len
        print "max_words_in_sentence: %d" % max_len


def generate_train_test():
    proj_name = "article_cat"
    db = ArticleDB()
    results = db.execute("select count(*) from article_cat")
    doc_num = results[0][0]
    results = db.execute("select id, category from article_cat order by id")
    db.close()

    train_num = int(doc_num * 0.8)
    test_num = int(doc_num * 0.2)

    max_len = 0
    with open("%s/seg_join/corpus.txt" % proj_name, "r") as corpus_file, \
            open("C:/Users/text_train.csv", "w") as train_file, \
            open("C:/Users/text_test.csv", "w") as test_file:
        corpus = corpus_file.readlines()
        new_corpus = []
        for line, row in zip(corpus, results):
            new_corpus.append('%d,%d,"%s"\n' % (row[1], row[0], line.strip()))
        from random import shuffle
        shuffle(new_corpus)

        train = new_corpus[0:train_num]
        test = new_corpus[train_num:train_num+test_num]

        train_file.writelines(train)
        test_file.writelines(test)

        for sen in train:
            cur_len = len(sen.split())
            if  cur_len > max_len:
                max_len = cur_len
        for sen in test:
            cur_len = len(sen.split())
            if  cur_len > max_len:
                max_len = cur_len
        print "max_words_in_sentence: %d" % max_len


def tag_count():
    proj_name = "article_cat"
    db = ArticleDB()
    cats = db.execute("select distinct category from %s order by category" % proj_name)
    cats = [row[0] for row in cats]
    for cat in cats:
        with open("tags/tag_%d.txt" % cat, "w") as tag_file:
            ids = db.execute("select id from %s where category=%d order by id" % (proj_name, cat))
            ids = [row[0] for row in ids]
            tag_dict = defaultdict(lambda: 0)
            has_tag = 0
            for id in ids:
                attr_name = "%s/attr/%d" %(proj_name, id)
                with open(attr_name, "r") as attr_file:
                    lines = attr_file.readlines()
                    tags = lines[3].strip()
                    if len(tags) > 0:
                        has_tag += 1
                        tags = tags.split(" ")
                        for tag in tags:
                            tag_dict[tag] += 1

            id_num = len(ids)
            tag_list = tag_dict.items()
            tag_list.sort(key=lambda x: x[1], reverse=True)
            tag_list = ["%s\t%d\n" % (tag, num) for tag, num in tag_list]
            tag_file.writelines(tag_list)
            print("category %d: %d/%d has tags" % (cat, has_tag, id_num))
    db.close()

def set_subcategory():
    proj_name = "article_cat"
    db = ArticleDB()
    cats = db.execute("select distinct category from %s order by category" % proj_name)
    cats = [row[0] for row in cats]
    for cat in cats:
        with open("tags/tag_%d.txt" % cat, "w") as tag_file:
            ids = db.execute("select id from %s where category=%d order by id" % (proj_name, cat))
            ids = [row[0] for row in ids]
            tag_dict = defaultdict(lambda: 0)
            has_tag = 0
            for id in ids:
                attr_name = "%s/attr/%d" % (proj_name, id)
                with open(attr_name, "r") as attr_file:
                    lines = attr_file.readlines()
                    tags = lines[3].strip()
                    if len(tags) > 0:
                        has_tag += 1
                        tags = tags.split(" ")
                        for tag in tags:
                            tag_dict[tag] += 1

            id_num = len(ids)
            tag_list = tag_dict.items()
            tag_list.sort(key=lambda x: x[1], reverse=True)
            tag_list = ["%s\t%d\n" % (tag, num) for tag, num in tag_list]
            tag_file.writelines(tag_list)
            print("category %d: %d/%d has tags" % (cat, has_tag, id_num))
    db.close()


def time_normalize(str_time, time_format='%Y-%m-%d %H:%M:%S'):
    ftime = time.mktime(time.strptime(str_time, time_format))
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ftime))


def time_normalize(str_time, time_format='%Y-%m-%d %H:%M:%S'):
    ftime = time.mktime(time.strptime(str_time, time_format))
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ftime))

if __name__ == "__main__":
    s = '{"errno":0,"data":{"total":0}}'
    json_obj = json.loads(s)
    l = json_obj["data"]["ari"]
    print l
