# coding=utf-8
from aliyunsdkcore.client import AcsClient

REGION = "cn-hangzhou"  # 暂时不支持多region
# ACCESS_KEY_ID/ACCESS_KEY_SECRET 根据实际申请的账号信息进行替换
ACCESS_KEY_ID = ""
ACCESS_KEY_SECRET = ""
acs_client = AcsClient(ACCESS_KEY_ID, ACCESS_KEY_SECRET, REGION)

# 需要接收的消息类型。短信回执：SmsReport，短息上行：SmsUp，语音呼叫：VoiceReport，流量直冲：FlowReport
msgtype = "SmsReport"
# 队列名称。在云通信页面开通相应业务消息后，就能在页面上获得对应的queueName
qname = "voson"

# 云通信固定的endpoint地址
endpoint = "https://1164630104358516.mns.cn-hangzhou.aliyuncs.com/"
