# coding=utf-8
import logging
import uuid
from logging.handlers import TimedRotatingFileHandler

from flask import Flask, g

from main.aliyun_sms.send_sms import send_sms

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


# 可能是由于要现有app，才能有routes这些，所以from import 放在了这里
# 路由
from .routes import *

# 模型
from .models import db, init_db

# 初始化数据库
# init_db()

# 记录日志
# 每间隔1D（天）滚动存档成一个日志，设置启用本地时间，而不是utc时间
handler = TimedRotatingFileHandler('learn_flask.log', when='D', interval=1, backupCount=0, encoding=None, delay=False,
                                   utc=False)
handler.setFormatter(logging.Formatter(
    '%(asctime)s  %(levelname)s  %(message)s  %(pathname)s  line %(lineno)d',
    # 设置显示时间的格式
    datefmt='%Y-%m-%d %H:%M:%S'
))
# 设置记录日志的等级，INFO 则 所有的日志记录都记录
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)

# send_sms(uuid.uuid1(), "13205173164", "松网", "SMS_101220014", "{\"code\":\"7894\"}")

# 如果Debug开启会被打印两遍
# print 3
