# coding=utf-8
import datetime
import json
from aliyunsdkcore.acs_exception.exceptions import ServerException
from main.aliyun_sms.aliyunsdkdybaseapi.request.v20170525.QueryTokenForMnsQueueRequest import \
    QueryTokenForMnsQueueRequest
from . import acs_client, msgtype


# 云通信业务token存在失效时间，需动态更新。
class Token():
    def __init__(self, token=None, tmp_access_id=None, tmp_access_key=None, expire_time=None):
        self.__token = token
        self.__tmp_access_id = tmp_access_id
        self.__tmp_access_key = tmp_access_key
        self.__expire_time = expire_time

    def get_token(self):
        return self.__token

    def set_token(self, token):
        self.__token = token

    def get_tmp_access_id(self):
        return self.__tmp_access_id

    def set_tmp_access_id(self, tmp_access_id):
        self.__tmp_access_id = tmp_access_id

    def get_tmp_access_key(self):
        return self.__tmp_access_key

    def set_tmp_access_key(self, tmp_access_key):
        self.__tmp_access_key = tmp_access_key

    def get_expire_time(self):
        return self.__expire_time

    def set_expire_time(self, expire_time):
        self.__expire_time = expire_time

    def is_refresh(self):
        # 失效时间与当前系统时间比较，提前2分钟刷新token
        now = datetime.datetime.now()
        expire = datetime.datetime.strptime(self.__expire_time, "%Y-%m-%d %H:%M:%S")
        # intval = (expire - now).seconds
        # print "token生效剩余时长（秒）：" + str(intval)
        if (expire - now).seconds < 120:
            return 1
        return 0

    def refresh(self):
        print "start refresh token..."
        request = QueryTokenForMnsQueueRequest()
        request.set_MessageType(msgtype)
        response = acs_client.do_action_with_exception(request)
        # print response
        if response is None:
            raise ServerException("GET_TOKEN_FAIL", "获取token时无响应")

        response_body = json.loads(response)

        if response_body.get("Code") != "OK":
            raise ServerException("GET_TOKEN_FAIL", "获取token失败")

        self.__tmp_access_key = response_body.get("MessageTokenDTO").get("AccessKeySecret")
        self.__tmp_access_id = response_body.get("MessageTokenDTO").get("AccessKeyId")
        self.__expire_time = response_body.get("MessageTokenDTO").get("ExpireTime")
        self.__token = response_body.get("MessageTokenDTO").get("SecurityToken")

        print "finsh refresh token..."
