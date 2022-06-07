import json

from websocket import WebSocketApp

from common.settings import Api
from core import msg


class Client:
    def __init__(self, user_id, token):
        self.user_id = user_id
        self.token = token
        # 初始化webSocket
        # websocket.enableTrace(True)
        ws_url = Api.ws_url() + f'?sendID={user_id}&token={token}&platformID=5'
        self.ws = WebSocketApp(url=ws_url)
        self.ws.on_open = self.__on_ws_open
        self.ws.on_error = self.__on_ws_error
        self.ws.on_message = self.__on_ws_message
        self.ws.on_close = self.__on_ws_close

        self.on_open = None
        self.on_error = None
        self.on_message = None
        self.on_data = None
        self.on_close = None

    def connect(self):
        self.ws.run_forever()

    def send(self, data):
        self.ws.send(json.dumps(data))
        print(f'ws send done., {data}')

    def __on_ws_open(self, obj):
        print('IM server websocket is connected!')
        self.on_open(obj)

    def __on_ws_error(self, obj, exception):
        print(f'[ON ERROR]:{exception}')
        self.on_error(obj, exception)

    def __on_ws_message(self, obj, data):
        print(f'[ON MESSAGE]:{data}')
        msg.handler_recv_message(data)
        self.on_message(data)

    def __on_ws_data(self, obj, data):
        print(f'[ON DATA]:{data}')
        self.on_data(data)

    def __on_ws_close(self, obj, code, msg):
        print(f'IM server websocket is close! close code:{code}, close message:{msg}')
        self.on_close(msg)
