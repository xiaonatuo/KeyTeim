import json
import math
import random
import threading
import time
from hashlib import md5

import uuid as uuid

from common import request
from common.client import Client
from common.settings import Api as apis
from core.msg import MsgWrapper


class User:
    """
    IM用户对象。包含了用户相关的操作，比如，登录、发送消息等
    """

    def __init__(self, user_id=None, pwd=None, name=None):
        """
        初始化一个用户

        Parameters:
            user_id: 用户ID
            pwd:用户密码（测试用例中暂时没有用到）
            name: 用户姓名 （测试用例中暂时没有用到）
        """
        self.user_id = user_id
        self.pwd = pwd
        self.name = name
        self.__token = None
        self.__client = None
        self.__msg_wrapper = None

    def login(self):
        """
        用户登录
        """
        assert self.user_id != '', '没有配置用户user_id'
        assert self.pwd != '', '没有配置用户pwd'
        if self.__token is None:
            self.__get_token()

        self.__client = Client(user_id=self.user_id, token=self.__token)
        self.__msg_wrapper = MsgWrapper(self, self.__client)
        self.__client.on_open = self.on_server_connected
        self.__client.on_message = self.on_server_message
        self.__client.connect()

    def __get_token(self):
        """
        获取用户token
        """
        data = {
            'secret': 'tuoyun',
            'platform': 5,
            'userId': self.user_id,
            'operationID': str(math.floor(time.time()))
        }
        res = request.post(url=apis.user_token(), body=data)
        self.__token = res.data()['token']
        print(self.__token)

    def on_server_connected(self, obj):
        """
        服务器连接成功事件回调函数
        """
        def send():
            data = json.dumps({'userID': self.user_id, 'token': self.__token})
            self.__client.send(self.__msg_wrapper.wrapper_data(data, 'Login'))
            content = input('请输入要发送的内容：')
            self.send_text_message('13391990902', content)

        threading.Thread(target=send).start()

    def on_server_message(self, message):
        """
        接收服务器消息
        """
        pass

    def send_text_message(self, recv_user, message):
        """
        发送文本消息

        Parameters:
            recv_user: 接收用户ID
            message: 要发送的消息
        """
        self.__msg_wrapper.send_text_message(recv_user, message)


