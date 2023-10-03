import re

import pymongo
from bson import ObjectId
from flask import Blueprint, request, render_template
from flask_paginate import Pagination, get_page_parameter

import StringView
from exts import mongo

# /auth
bp = Blueprint("qa", __name__, url_prefix="/")


@bp.route("/")
# 主界面
def index():
    per_page = int(request.args.get('per_page', 10)) # 每一页显示数量
    # 获取当前为第几页
    page = request.args.get(get_page_parameter(), type=int, default=1)
    url_count = mongo.db.acl_bibs.count_documents({})
    # 获取当前页内容查询结果
    results = mongo.db.acl_bibs.find({}).sort([('year', pymongo.DESCENDING), ('month', pymongo.DESCENDING)]).skip((page-1)*per_page).limit(per_page)
    # 处理多余字符
    arr = []
    for result in results:
        arr.append(result)
    arr_result = StringView.StringView(arr)  #数组接收处理完后的结果
    #实行分页
    pagination = Pagination(bs_version=4, page=page, per_page=per_page, total=url_count)
    return render_template("index.html", arrays=arr_result, pagination=pagination)


@bp.route("/search")
# 搜索页面
def search():
    q = request.args.get("q")
    #搜索：正则表达式，返回标题和摘要中带有关键词的文章
    #todo：排序优化
    q1 = re.compile(q, re.I)
    results = mongo.db.acl_bibs.find({"title": {'$regex': q1}, "abstract": {'$regex': q1}}).sort("year", pymongo.DESCENDING).limit(10)
    # 处理多余字符
    arr = []
    for result in results:
        arr.append(result)
    arr_result = StringView.StringView(arr)  # 数组接收处理完后的结果
    return render_template("index.html", arrays=arr_result)


@bp.route("/qa/detail/<qa_id>")
# 单篇论文的详细页面显示
def qa_detail(qa_id):
    details = mongo.db.acl_bibs.find_one({"_id": ObjectId(qa_id)})
    details = StringView.DictView(details) #处理多余字符
    return render_template("detail.html", details=details)


@bp.route("/keyword/detail/")
# 关键词相关论文
def keyword_detail():
    #details = mongo.db.acl_bibs.find({"keyword": keyword_name})
    return render_template("keyword.html")


@bp.route("/method/detail/<method_name>")
#研究方法相关论文
def method_detail(method_name):
    details = mongo.db.acl_bibs.find({"method": method_name})
    return render_template("method.html", method_name=method_name, details=details)

@bp.route("/merics/detail/<merics_name>")
#merics相关论文
def merics_detail(merics_name):
    details = mongo.db.acl_bibs.find({"merics": merics_name})
    return render_template("merics.html", merics_name=merics_name, details=details)

@bp.route("/task/detail/<task_name>")
#研究任务相关论文
def task_detail(task_name):
    details = mongo.db.acl_bibs.find({"task": task_name})
    return render_template("task.html", task_name=task_name, details=details)


@bp.route("/dataset/detail/<dataset_name>")
#数据集相关论文
def dateset_detail(dataset_name):
    details = mongo.db.acl_bibs.find({"dataset": dataset_name})
    return render_template("dataset.html", dataset_name=dataset_name, details=details)


