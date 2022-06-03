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


class User:
    """IM用户对象。

    包含了用户相关的操作，比如，登录、发送消息等

    :argument
        user_id: 用户ID
        pwd: 登录密码
        name: 用户姓名
    """

    def __init__(self, user_id=None, pwd=None, name=None):
        self.user_id = user_id
        self.pwd = pwd
        self.name = name
        self.token = None
        self.client = None

    def login(self):
        assert self.user_id != '', '没有配置用户user_id'
        assert self.pwd != '', '没有配置用户pwd'
        if self.token is None:
            self.get_token()

        self.client = Client(user_id=self.user_id, token=self.token)
        self.client.on_open(self.client_on_open)
        self.client.connect()

    def get_token(self):
        data = {
            'secret': 'tuoyun',
            'platform': 5,
            'userId': self.user_id,
            'operationID': str(math.floor(time.time()))
        }
        res = request.post(url=apis.user_token(), body=data)
        self.token = res.data()['token']
        print(self.token)

    def client_on_open(self, obj):
        def send():
            data = json.dumps({'userID': self.user_id, 'token': self.token})
            self.client.send(self.build_send_data(data, 'Login'))
            content = input('请输入要发送的内容：')
            self.create_text_message(content)
        threading.Thread(target=send).start()

    def create_text_message(self, text):
        self.client.send(self.build_send_data(text, 'CreateTextMessage'))

    def send_message(self, message):
        params = {
            "recvID": "15810743632",
            "groupID": "",
            "offlinePushInfo": None,
            "message": json.dumps(message),
        }
        self.client.send(params)

    def build_send_data(self, data, func_name):
        rand = math.floor(random.Random().random() * 10000)
        return {
            'reqFuncName': func_name,
            'operationID': str(math.floor(time.time())) + f'{rand}',
            'userID': self.user_id,
            'data': data,
        }
