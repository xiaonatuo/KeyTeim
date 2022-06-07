import json
import math
import random
import time

# 发送消息等事件操作的回调函数的缓存
__operate_cache__ = {}


def handler_recv_message(message):
    """
    处理接收到的服务器消息

    Parameters:
        message: 服务器消息
    """
    data = json.loads(message)
    if 'CreateTextMessage' == data['event']:
        callback = __operate_cache__[data['operationID']]
        assert callable(callback), 'create text message callback is not a function!'
        callback(data['data'])


class MsgWrapper:
    """
    IM消息封装器
    """

    def __init__(self, user, ws_client):
        """
        Parameters:
            user: user
                当前用户
            ws_client: client
                web socket 客户端
        """
        self.user = user
        self.ws_client = ws_client

    def send_text_message(self, recv_user, text_msg):
        """
        发送文本消息

        Parameters:
            recv_user: 消息接收用户
            text_msg: 消息内容
        """

        def send_message(message):
            push_info = self.wrapper_push_info(text_msg)
            data = {
                "recvID": recv_user,
                "groupID": "",
                "offlinePushInfo": push_info,
                "message": message,
            }
            self.ws_client.send(self.wrapper_data(json.dumps(data), 'SendMessage'))

        operate_id = self.create_message(text_msg, 'CreateTextMessage')
        __operate_cache__[operate_id] = send_message

    def create_message(self, text_msg, func_name):
        """
        向IM服务器发送创建一个文本消息的请求

        Parameters:
            text_msg: 文本类型的消息
            func_name: 对应的功能名称

        Return:
            操作ID
        """
        data = self.wrapper_data(text_msg, func_name)
        self.ws_client.send(data)
        return data['operationID']

    def wrapper_data(self, data, func_name):
        """
        封装要发送的数据

        Parameters:
            data: 要封装的数据
            func_name: 本次发送的数据的功能名称

        Return:
            封装后的数据
        """
        rand = math.floor(random.Random().random() * 10000)
        return {
            'reqFuncName': func_name,
            'operationID': self.user.user_id + '_' + str(math.floor(time.time())) + f'{rand}',
            'userID': self.user.user_id,
            'data': data,
        }

    @staticmethod
    def wrapper_push_info(msg):
        return json.dumps({
                    "title": "你收到一条消息",
                    "desc": msg,
                    "ex": "",
                    "iOSPushSound": "+1",
                    "iOSBadgeCount": True
                })
