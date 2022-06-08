import _thread
import json
import math
import time

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
        self.on_msg = None
        self.__token = None
        self.__client = None
        self.__msg_wrapper = None
        self.login_callback = None

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

        _thread.start_new_thread(self.__client.connect, ())

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

    def on_server_connected(self, obj):
        """
        服务器连接成功事件回调函数
        """
        print(f'服务器连接成功>>>>>>【{self.user_id}】')
        data = json.dumps({'userID': self.user_id, 'token': self.__token})
        self.__client.send(self.__msg_wrapper.wrapper_data(data, 'Login'))

    def on_server_message(self, message):
        """
        接收服务器消息
        """
        msg_obj = json.loads(message)
        event = msg_obj['event']
        if event == 'Login' and msg_obj['errCode'] == 0:
            print(f'用户登录成功>>>>>>【{self.user_id}】')
            if callable(self.login_callback):
                self.login_callback()
        else:
            data = json.loads(msg_obj['data'])
            content = data['content']
            # print(f'recv<<<<<<【{self.user_id}】接收到了一条消息：{content}')
            self.on_msg(content)

    def send_text_message(self, recv_user, message):
        """
        发送文本消息

        Parameters:
            recv_user: 接收用户ID
            message: 要发送的消息
        """
        self.__msg_wrapper.send_text_message(recv_user, message)
        print(f'send>>>>>>【{self.user_id}】向【{recv_user}】发送了消息：{message}')

    def logout(self):
        self.__client.close()
