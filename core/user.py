import math
import time

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

    def login(self):
        assert self.user_id != '', '没有配置用户user_id'
        assert self.pwd != '', '没有配置用户pwd'
        if self.token is None:
            self.get_token()

        # 通过webSocket登录
        print(self.token)
        client = Client(user_id=self.user_id, token=self.token)
        client.connect()

    def get_token(self):
        data = {
            'secret': 'tuoyun',
            'platform': 1,
            'userId': self.user_id,
            'operationID': str(math.floor(time.time()))
        }
        res = request.post(url=apis.user_token(), body=data)
        self.token = res.data()['token']
