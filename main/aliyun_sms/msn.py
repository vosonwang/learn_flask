# coding=utf-8
from mns.account import Account
from mns.queue import *
from .Token import Token
from . import endpoint,qname
import sys


# 初始化 my_account, my_queue
token = Token()
token.refresh()
my_account = Account(endpoint, token.get_tmp_access_id(), token.get_tmp_access_key(), token.get_token())
my_queue = my_account.get_queue(qname)

# my_queue.set_encoding(False)
# 循环读取删除消息直到队列空
# receive message请求使用long polling方式，通过wait_seconds指定长轮询时间为3秒

## long polling 解析:
### 当队列中有消息时，请求立即返回；
### 当队列中没有消息时，请求在MNS服务器端挂3秒钟，在这期间，有消息写入队列，请求会立即返回消息，3秒后，请求返回队列没有消息；

wait_seconds = 3
print "%sReceive And Delete Message From Queue%s\nQueueName:%s\nWaitSeconds:%s\n" % (
    10 * "=", 10 * "=", qname, wait_seconds)
while True:
    # 读取消息
    try:
        # token过期是否需要刷新
        if token.is_refresh() == 1:
            # 刷新token
            token.refresh()
            my_account.mns_client.close_connection()
            my_account = Account(endpoint, token.get_tmp_access_id(), token.get_tmp_access_key(), token.get_token())
            my_queue = my_account.get_queue(qname)

        # 接收消息
        recv_msg = my_queue.receive_message(wait_seconds)

        # TODO 业务处理

        print "Receive Message Succeed! ReceiptHandle:%s MessageBody:%s MessageID:%s" % (
            recv_msg.receipt_handle, recv_msg.message_body, recv_msg.message_id)

    except MNSExceptionBase, e:
        if e.type == "QueueNotExist":
            print "Queue not exist, please create queue before receive message."
            sys.exit(0)
        elif e.type == "MessageNotExist":
            print "Queue is empty! sleep 10s"
            time.sleep(10)
            continue
        print "Receive Message Fail! Exception:%s\n" % e
        continue

    # 删除消息
    try:
        my_queue.delete_message(recv_msg.receipt_handle)
        print "Delete Message Succeed!  ReceiptHandle:%s" % recv_msg.receipt_handle
    except MNSExceptionBase, e:
        print "Delete Message Fail! Exception:%s\n" % e