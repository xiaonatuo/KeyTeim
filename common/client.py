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

    def close(self):
        self.ws.close()

    def __on_ws_open(self, obj):
        if callable(self.on_open):
            self.on_open(obj)

    def __on_ws_error(self, obj, exception):
        if callable(self.on_error):
            self.on_error(obj, exception)

    def __on_ws_message(self, obj, data):
        new_msg = msg.handler_recv_message(data)
        if new_msg is not None and new_msg != '' and callable(self.on_message):
            self.on_message(new_msg)

    def __on_ws_data(self, obj, data):
        if callable(self.on_data):
            self.on_data(data)

    def __on_ws_close(self, obj, code, msg):
        if callable(self.on_close):
            self.on_close(msg)
