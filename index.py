# coding=utf-8
import numpy as np
import random
from flask import Flask, render_template, request, jsonify
import time
from category import Category
import sys
from articledb import ArticleDB
from article import ArticleDumper
from myutils import TopkHeap
from sklearn.metrics.pairwise import cosine_similarity
reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)

db = ArticleDB()

project_name = "article15081608"
txt_dir = project_name + "/txt/"
attr_dir = project_name + "/attr/"
category_dict = Category()
thumbs = [
    "063226153482.jpg",
    "071142757085.jpg",
    "072728052607.jpg",
    "073704072438.jpg",
    "081042492216.jpg",
    "090854778371.jpeg",
    "092220134851.jpg",
    "102652963888.png",
    "103550760868.jpg",
    "111531748717.jpg",
    "112713761995.png",
    "123006128256.jpg",
    "123641032783.jpg",
    "125123423041.jpg",
    "125425018839.png",
    "143948746006.jpg",
    "144655265068.jpg",
    "152502600146.jpg",
    "160004485992.png",
    "171128413415.jpg",
    "210804890144.png",
    "220548955698.jpg",
    "224636881111.jpg",
    "230826808516.png"
]


doc_num = db.execute("select count(*) from %s" % project_name)[0][0]
all_articles = [None] * doc_num
for i in xrange(doc_num):
    obj_name = "%s/obj/%d" % (project_name, i + 1)
    all_articles[i] = ArticleDumper.load(obj_name)


# 文章列表：主页分页
@app.route('/')
def main():
    category_id = 0
    eng_category = request.args.get('category')
    if (eng_category is not None) and (category_dict.e2n[eng_category.encode("utf-8")] is not None):
        category_id = category_dict.e2n[eng_category.encode("utf-8")]
        sql = "select id, category from %s where category = %d order by time desc limit 0,10" % (
            project_name, category_id)
    else:
        sql = "select id, category from %s order by time desc limit 0,10" % project_name
    results = db.execute(sql)
    article_infos = []
    for a_id, a_category in results:
        a_digest = ""
        attr_name = attr_dir + str(a_id)
        txt_name = txt_dir + str(a_id)
        with open(attr_name, "r") as attr_file:
            lines = attr_file.readlines()
            a_time = lines[0]
            a_title = lines[1]
            a_url = lines[2]
            a_tags = lines[3]
        with open(txt_name, "r") as txt_file:
            txt_file.readline()
            txt_file.readline()
            for line in txt_file:
                if len(line) > 20:
                    a_digest = line.decode("utf-8")[:30].encode("utf-8") + "......"

        chn_category = category_dict.n2c[a_category]
        eng_category = category_dict.n2e[a_category]
        thumb_name = thumbs[random.randint(0, len(thumbs)-1)]
        article_infos.append([a_id, a_time, a_title, a_url, a_digest, a_tags, a_category, chn_category, eng_category, thumb_name])
        last_dateline = article_infos[-1][1]
    return render_template('index.html', article_infos=article_infos, catid=category_id, last_dateline=last_dateline)


# 文章正文
@app.route('/article/')
def article():
    article_id = request.args.get('article_id')
    if article_id is not None:
        # 获取文章ID和类别ID
        article_id = int(article_id.encode("utf-8"))
        sql = "select id, category from %s where id = %d" % (project_name, article_id)
        results = db.execute(sql)
        a_id = results[0][0]
        a_category = results[0][1]
        a_text = None

        # 获取文章时间，URL，标签，正文
        attr_name = attr_dir + str(a_id)
        txt_name = txt_dir + str(a_id)
        with open(attr_name, "r") as attr_file:
            lines = attr_file.readlines()
            a_time = lines[0]
            a_title = lines[1]
            a_url = lines[2]
            a_tags = lines[3]
        with open(txt_name, "r") as txt_file:
            txt_file.readline()
            txt_file.readline()
            a_text = txt_file.readlines()

        # 文章类别ID对应的中文和英文名称
        chn_category = category_dict.n2c[a_category]
        eng_category = category_dict.n2e[a_category]
        article_info = [a_id, a_time, a_title, a_url, a_text, a_tags, a_category, chn_category, eng_category]

        # 相似文章
        tokheap = TopkHeap(5)
        now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        sql = "select id from %s where time < '%s' and category=%d limit 0,100" % (project_name, now_time, a_category)
        target_article = ArticleDumper.load("%s/obj/%d" % (project_name, a_id))
        results = db.execute(sql)
        for a_id in results:
            a_id = a_id[0]
            src = target_article
            dst = all_articles[a_id-1]
            similarity = cosine_similarity(np.asarray(src.a_text), np.asarray(dst.a_text))
            tokheap.push((dst, similarity), lambda x, y: x[1] > y[1])
        tok_articles = tokheap.topk()
        tok_articles = [item[0] for item in tok_articles]

        return render_template('article_index.html', article_info=article_info, tok_articles=tok_articles)
    else:
        return ""


# 文章列表，动态获取
@app.route('/v2_action/article_list', methods=['GET', 'POST'])
def article_list():
    catid = int(request.form.get('catid', 0).encode("utf-8"))
    last_dateline = request.form.get('last_dateline', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    if catid > 0:
        sql = "select id, category from %s where category = %d and time < '%s' order by time desc limit 0,10" % (
            project_name, catid, last_dateline)
    elif catid == 0:
        sql = "select id, category from %s where time < '%s' order by time desc limit 0,10" % (
            project_name, last_dateline)
    else:
        return ""

    results = db.execute(sql)
    article_infos = []
    for a_id, a_category in results:
        a_digest = ""
        attr_name = attr_dir + str(a_id)
        txt_name = txt_dir + str(a_id)
        with open(attr_name, "r") as attr_file:
            lines = attr_file.readlines()
            a_time = lines[0]
            a_title = lines[1]
            a_url = lines[2]
            a_tags = lines[3]
        with open(txt_name, "r") as txt_file:
            txt_file.readline()
            txt_file.readline()
            for line in txt_file:
                if len(line) > 20:
                    a_digest = line.decode("utf-8")[:30].encode("utf-8") + "......"

        chn_category = category_dict.n2c[a_category]
        eng_category = category_dict.n2e[a_category]
        thumb_name = thumbs[random.randint(0, len(thumbs) - 1)]
        article_infos.append(
            [a_id, a_time, a_title, a_url, a_digest, a_tags, a_category, chn_category, eng_category, thumb_name])
    data = render_template('article_list.html', article_infos=article_infos)

    if len(article_infos) > 0:
        result = 1
        last_dateline = article_infos[-1][1]
    else:
        result = 0
        last_dateline = "1970-01-01 08:00:00"
    jdata = {
        'result': result,
        'msg': '已经没有更多信息了',
        'data': data,
        'total_page': 975,
        'last_dateline': last_dateline
    }
    return jsonify(jdata)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
