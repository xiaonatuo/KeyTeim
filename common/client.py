import asyncio
import json
import math
import time
from uuid import UUID

import websocket
from websocket import WebSocketApp

from common.settings import Api


class Client:
    def __init__(self, user_id, token):
        self.user_id = user_id
        self.token = token
        data = {'userID': user_id, 'token': token}
        self.params = {
            'userID': user_id,
            'reqFuncName': 'Login',
            'operationID': str(math.floor(time.time())),
            'data': json.dumps(data),

        }
        websocket.enableTrace(True)
        self.ws = WebSocketApp(Api.ws_url())
        self.ws.header = {
            'platformID': 5,
            'token': token,
            'sendID': user_id
        }
        self.ws.on_open = self.on_open
        self.ws.on_error = self.on_error

    def connect(self):
        self.ws.run_forever()

    def send(self, data):
        self.ws.send(data)

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

    def on_close(self, obj, code, msg):
        if callable(obj):
            self.ws.on_close = obj
        else:
            print(f'IM server websocket is close! close code:{code}, close message:{msg}')
