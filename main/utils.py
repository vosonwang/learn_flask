# coding=utf-8
from flask import json


def json_package(a, b):
    """将结果转成json"""
    return json.dumps({'Status': a, 'Result': b}, ensure_ascii=False)
