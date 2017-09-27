# coding=utf-8
from flask import Flask, g

# def create_app():

# instance_relative_config，默认为False，如果设置为True的话，他会将配置文件路径设置为实例文件的路径，而不是应用程序根目录
app = Flask(__name__, instance_relative_config=True)

app.config.from_object('config')

# silent=True 表示如果配置文件不存在的时候不抛出异常,默认是为 False,会抛出异常
app.config.from_pyfile('config.py', silent=True)


# 每一次请求到来后，都会先执行它
@app.before_request
def before_request():
    g.session = db.session


# 每一次请求结束，如果请求没有异常，都会先执行它
# @app.after_request
# def after_request():
#     # pass是占位符
#     pass


# 请求处理的最后执行 teardown_request() 函数。这类函数在任何情况下都会被执行，甚至是在发生未处理异常或请求预处理器没有执行（ 例如在测试环境下，有时不想执行）的情况下。
# 关闭数据库连接
@app.teardown_request
def teardown_request(exception):
    g.session.close()


# 路由
from .routes import *
# 模型
from models import db

# 创建表
# db.create_all()
