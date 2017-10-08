# coding=utf-8
from main import app
from .models import *
from flask import request, json
from .utils import json_package
import re


@app.route('/notes', methods=['POST', 'PUT', 'PATCH'])
def __save_note():
    """保存笔记"""
    try:
        b = request.data
        if b:
            d = json.loads(b)
            if request.method == 'POST':
                return json_package('success', save_note(d))
            else:
                "更新全部或部分内容"
                return json_package('success', update_note(d['short_id'], d['text']))

    except Exception, e:
        app.logger.error('%s %s %s ' + e.message, request.remote_addr, request.method,
                         request.base_url.encode('unicode-escape'))
        return json_package('error', e.message)
    else:
        return json_package('warning', '客户端未传数据')


@app.route('/notes/<short_id>', methods=['GET'])
def __find_note(short_id):
    """根据short_id查找笔记"""
    try:
        if re.match(r'\d{1,4}$', short_id) is not None and find_note(short_id) is not None:
            return json_package('success', find_note(short_id))
    except Exception, e:
        app.logger.error('%s %s %s ' + e.message, request.remote_addr, request.method,
                         request.base_url.encode('unicode-escape'))
        return json_package('error', e.message)
    else:
        return json_package('warning', '查无此记录')


@app.route('/notes', methods=['GET'])
def __all_notes():
    """获取所有笔记"""
    return json_package('success', all_notes())

@app.route('/notes/<short_id>', methods=['DELETE'])
def __delete_note(short_id):
    """删除笔记"""
    try:
        if delete_note(short_id) is None:
            return json_package('success', '删除成功')
    except Exception, e:
        app.logger.error('%s %s %s ' + e.message, request.remote_addr, request.method,
                         request.base_url.encode('unicode-escape'))
        return json_package('error', e.message)
    else:
        return json_package('error', '查无此记录')


@app.route('/notes', methods=['DELETE'])
def ___delete_notes():
    """批量删除笔记"""
    try:
        b = request.data
        if b:
            if batch_delete(json.loads(b)['short_ids']) > 0:
                # %s是字符串占位符 %d是数字占位符 info('%s %s %s %s'+msg,<tuple>(a,b,c,d))
                app.logger.info('%s %s %s short_id: %s', request.remote_addr, request.method,
                                request.base_url.encode('unicode-escape'), json.loads(b)['short_ids'])
                return json_package('success', '删除成功')
            else:
                return json_package('success', '删除失败')
    except Exception, e:
        app.logger.error('%s %s %s ' + e.message, request.remote_addr, request.method,
                         request.base_url.encode('unicode-escape'))
        return json_package('error', e.message)


@app.errorhandler(404)
def page_not_found(error):
    return json_package('error', error.description)


@app.errorhandler(405)
def page_not_found(error):
    return json_package('error', error.description)


@app.errorhandler(500)
def page_not_found(error):
    return json_package('Error', error.description)


# 暂时不知道下面这个什么时候会用到
@app.errorhandler(Exception)
def unhandled_exception(error):
    app.logger.error('Unhandled Exception: %s', error)
