import json

import websocket
from websocket import WebSocketApp

from common.settings import Api


class Client:
    def __init__(self, user_id, token):
        self.user_id = user_id
        self.token = token
        # 初始化webSocket
        #websocket.enableTrace(True)
        ws_url = Api.ws_url() + f'?sendID={user_id}&token={token}&platformID=5'
        self.ws = WebSocketApp(url=ws_url)
        self.ws.on_open = self.on_open
        self.ws.on_error = self.on_error
        self.ws.on_message = self.on_message
        self.ws.on_close = self.on_close

    def connect(self):
        self.ws.run_forever(ping_timeout=1)

    def send(self, data):
        self.ws.send(json.dumps(data))
        self.ws.on_message = self.on_message
        print(f'ws send done., {data}')

    def on_open(self, obj):
        if callable(obj):
            self.ws.on_open = obj
        else:
            print('IM server websocket is connected!')

    def on_error(self, obj, exception):
        if callable(obj):
            self.ws.on_error = obj
        else:
            print(f'[ON ERROR]:{exception}')

    def on_message(self, obj, data):
        if callable(obj):
            self.ws.on_message = obj
        else:
            print(f'[ON MESSAGE]:{data}')

    def on_data(self, obj, data):
        if callable(obj):
            self.ws.on_data = obj
        else:
            print(f'[ON DATA]:{data}')

    def on_close(self, obj, code, msg):
        if callable(obj):
            self.ws.on_close = obj
        else:
            print(f'IM server websocket is close! close code:{code}, close message:{msg}')
