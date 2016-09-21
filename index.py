# coding=utf-8
import numpy as np
import random
from flask import Flask, render_template, request, jsonify, render_template, url_for, send_from_directory
from flask import send_file
import time
from myutils import Category, CompareUnit, read_subcat, read_subclt
import sys
from myutils import ArticleDB
from myutils import TopkHeap, Dumper
from sklearn.metrics.pairwise import cosine_similarity
from treelib import Tree

reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)

db = ArticleDB()

project_name = "article150801160830"
# project_name = "article_cat"
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

# 加载tfidf对象文件
doc_num = db.execute("select count(*) from %s" % project_name)[0][0]
tfidf_vectors = [0.0] * doc_num
# for i in xrange(doc_num):
#     print "\rloading %d/%d" % (i, doc_num),
#     obj_name = "%s/clf_tfidf/%d" % (project_name, i + 1)
#     tfidf_vectors[i] = Dumper.load(obj_name)
# print ""

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

cat2subcat, tag2id = read_subcat("subcat")
subclt_offset, cat2subclt = read_subclt("subclt")


# 分类版：文章列表首页
@app.route('/')
def main():
    category_id = 0
    subcate_id = 0
    eng_category = request.args.get('category')
    subcategory = request.args.get('subcategory')
    if eng_category is not None and subcategory is not None:
        category_id = category_dict.e2n[eng_category.encode("utf-8")]
        subcate_id = int(subcategory.encode("utf-8"))
        sql = "select id, category from %s where category=%d and subcategory=%d order by time desc limit 0,10" % (
            project_name, category_id, subcate_id)
    elif eng_category is not None:
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
        thumb_name = thumbs[random.randint(0, len(thumbs) - 1)]
        article_infos.append(
            [a_id, a_time, a_title, a_url, a_digest, a_tags, a_category, chn_category, eng_category, thumb_name])
    last_dateline = article_infos[-1][1]
    return render_template('index.html', article_infos=article_infos, catid=category_id, subcatid=subcate_id, last_dateline=last_dateline, category=Category(), cat2subcat=cat2subcat)


# 分类版：文章列表次页（动态获取）
@app.route('/article_list', methods=['GET', 'POST'])
def article_list():
    catid = int(request.form.get('catid', 0).encode("utf-8"))
    subcatid = int(request.form.get('subcatid', 0).encode("utf-8"))
    last_dateline = request.form.get('last_dateline', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    if catid > 0 and subcatid > 0:
        sql = "select id, category from %s where category = %d and subcategory = %d and time < '%s' order by time desc limit 0,10" % (
            project_name, catid, subcatid, last_dateline)
    elif catid > 0:
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
        with open(attr_name, "r") as attr_file, open(txt_name, "r") as txt_file:
            lines = attr_file.readlines()
            a_time = lines[0]
            a_title = lines[1]
            a_url = lines[2]
            a_tags = lines[3]
            txt_file.readline()
            txt_file.readline()
            for line in txt_file:
                if len(line) > 20:
                    a_digest = line.decode("utf-8")[:30].encode("utf-8") + "......"
                    break

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


# 聚类版：文章列表首页
@app.route('/v2/')
def main_v2():
    category_id = 0
    cat1 = request.args.get('cat1')
    cat2 = request.args.get('cat2')
    if cat2 is not None:
        cat2 = int(cat2.encode("utf-8"))
        sql = "select id, category1, category2 from %s where category2=%d order by time desc limit 0,10" % \
              (project_name, cat2)
    elif cat1 is not None:
        cat1 = int(cat1.encode("utf-8"))
        sql = "select id, category1, category1 from %s where category1=%d order by time desc limit 0,10" % \
              (project_name, cat1)
    else:
        sql = "select id, category1, category2 from %s order by time desc limit 0,10" % project_name
    results = db.execute(sql)

    article_infos = []
    for a_id, a_cate1, a_cate2 in results:
        a_digest = ""
        attr_name = attr_dir + str(a_id)
        txt_name = txt_dir + str(a_id)
        with open(attr_name, "r") as attr_file, open(txt_name, "r") as txt_file:
            lines = attr_file.readlines()
            a_time = lines[0]
            a_title = lines[1]
            a_url = lines[2]
            a_tags = lines[3]
            txt_file.readline()
            txt_file.readline()
            for line in txt_file:
                if len(line) > 20:
                    a_digest = line.decode("utf-8")[:30].encode("utf-8") + "......"
                    break

        thumb_name = thumbs[random.randint(0, len(thumbs) - 1)]
        article_infos.append(
            [a_id, a_time, a_title, a_url, a_digest, a_tags, a_cate1, str(a_cate1), a_cate2, str(a_cate2), thumb_name])
    last_dateline = article_infos[-1][1]

    # 添加二级文章类别横条
    header1_list = [node.tag for node in cat_tree.children(-1)]
    header2_list = []
    for header_item in header1_list:
        children = cat_tree.children(header_item[0])
        header2_list.append([node.tag for node in children])

    return render_template('index_v2.html', article_infos=article_infos, catid=category_id, last_dateline=last_dateline,
                           header1_list=header1_list, header2_list=header2_list,
                           cat1=-1 if cat1 is None else cat1,
                           cat2=-1 if cat2 is None else cat2)


# 聚类版：文章列表次页（动态获取）
@app.route('/v2/article_list', methods=['GET', 'POST'])
def article_list_v2():
    cat1 = int(request.form.get('cat1', u"-1").encode("utf-8"))
    cat2 = int(request.form.get('cat2', u"-1").encode("utf-8"))
    last_dateline = request.form.get('last_dateline', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    if cat2 >= 0:
        sql = "select id, category1, category2 from %s where category2=%d and time < '%s' order by time desc limit 0,10" % (
            project_name, cat2, last_dateline)
    elif cat1 >= 0:
        sql = "select id, category1, category2 from %s where category1=%d and time < '%s' order by time desc limit 0,10" % (
            project_name, cat1, last_dateline)
    else:
        sql = "select id, category1, category2 from %s where time < '%s' order by time desc limit 0,10" % (
            project_name, last_dateline)

    results = db.execute(sql)
    article_infos = []
    for a_id, a_cate1, a_cate2 in results:
        a_digest = ""
        attr_name = attr_dir + str(a_id)
        txt_name = txt_dir + str(a_id)
        with open(attr_name, "r") as attr_file, open(txt_name, "r") as txt_file:
            lines = attr_file.readlines()
            a_time = lines[0]
            a_title = lines[1]
            a_url = lines[2]
            a_tags = lines[3]
            txt_file.readline()
            txt_file.readline()
            for line in txt_file:
                if len(line) > 20:
                    a_digest = line.decode("utf-8")[:30].encode("utf-8") + "......"
                    break
        thumb_name = thumbs[random.randint(0, len(thumbs) - 1)]
        article_infos.append(
            [a_id, a_time, a_title, a_url, a_digest, a_tags, a_cate1, str(a_cate1), a_cate2, str(a_cate2), thumb_name])
    data = render_template('article_list_v2.html', article_infos=article_infos)

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


# 分类+聚类版：文章列表首页
@app.route('/v3/')
def main_v3():
    category_id = 0
    subclt_id = 0
    eng_category = request.args.get('category')
    subcluster = request.args.get('subcluster')
    if eng_category is not None and subcluster is not None:
        category_id = category_dict.e2n[eng_category.encode("utf-8")]
        subclt_id = int(subcluster.encode("utf-8"))
        sql = "select id, category from %s where category=%d and subcluster=%d order by time desc limit 0,10" % (
            project_name, category_id, subclt_id)
    elif eng_category is not None:
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
        thumb_name = thumbs[random.randint(0, len(thumbs) - 1)]
        article_infos.append(
            [a_id, a_time, a_title, a_url, a_digest, a_tags, a_category, chn_category, eng_category, thumb_name])
    last_dateline = article_infos[-1][1]
    return render_template('index_v3.html', article_infos=article_infos, catid=category_id, subcltid=subclt_id, last_dateline=last_dateline, category=Category(), cat2subclt=cat2subclt)


# 分类+聚类版：文章列表次页（动态获取）
@app.route('/v3/article_list', methods=['GET', 'POST'])
def article_list_v3():
    catid = int(request.form.get('catid', u'0').encode("utf-8"))
    subcltid = int(request.form.get('subcltid', u'0').encode("utf-8"))
    last_dateline = request.form.get('last_dateline', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    if catid > 0 and subcltid > 0:
        sql = "select id, category from %s where category = %d and subcluster = %d and time < '%s' order by time desc limit 0,10" % (
            project_name, catid, subcltid, last_dateline)
    elif catid > 0:
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
        with open(attr_name, "r") as attr_file, open(txt_name, "r") as txt_file:
            lines = attr_file.readlines()
            a_time = lines[0]
            a_title = lines[1]
            a_url = lines[2]
            a_tags = lines[3]
            txt_file.readline()
            txt_file.readline()
            for line in txt_file:
                if len(line) > 20:
                    a_digest = line.decode("utf-8")[:30].encode("utf-8") + "......"
                    break

        chn_category = category_dict.n2c[a_category]
        eng_category = category_dict.n2e[a_category]
        thumb_name = thumbs[random.randint(0, len(thumbs) - 1)]
        article_infos.append(
            [a_id, a_time, a_title, a_url, a_digest, a_tags, a_category, chn_category, eng_category, thumb_name])
    data = render_template('article_list_v3.html', article_infos=article_infos)

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
        sql = "select id from %s where time < '%s' and category=%d and id!=%d limit 0,100" % (
            project_name, now_time, a_category, article_id)
        src_vector = tfidf_vectors[article_id - 1]
        results = db.execute(sql)
        for row in results:
            a_id = row[0]
            dst_vector = tfidf_vectors[a_id - 1]
            similarity = cosine_similarity(src_vector, dst_vector)[0][0]
            tokheap.push(CompareUnit(similarity, a_id))
        topk_article_ids = [x.value for x in tokheap.topk()]

        topk_articles = []
        for a_id in topk_article_ids:
            attr_name = attr_dir + str(a_id)
            with open(attr_name, "r") as attr_file:
                lines = attr_file.readlines()
                a_time = lines[0]
                a_title = lines[1]
                a_url = lines[2]
                a_tags = lines[3]
            thumb_name = thumbs[random.randint(0, len(thumbs) - 1)]
            topk_articles.append([a_id, a_time, a_title, a_url, a_tags, thumb_name])

        return render_template('article_index.html', article_info=article_info, topk_articles=topk_articles)
    else:
        return ""


@app.route('/png')
def png():
    return send_from_directory('static', 'myresources/tdidf_clf_precision.png', mimetype='image/jpg')


@app.route('/txt')
def txt():
    return send_from_directory('static', 'myresources/tdidf_clf_precision.txt')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
