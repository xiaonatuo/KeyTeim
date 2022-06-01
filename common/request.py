import json
import requests


def send(url, method, body=None, headers=None, token=None):
    """
    发送请求
    :param url: 请求地址，
    :param method: 请求方法
    :param body: 请求体
    :param headers: 请求头
    :param token: 认证token
    :return: ApiRes对象
    """
    # 设置请求头
    if headers is not None:
        if headers['token'] is None and token is not None:
            headers['token'] = token

    # 设置请求数据
    data = body
    if body is not None:
        data = json.dumps(body)

    response = requests.request(method, url, data=data, headers=headers)
    return ApiRes(response)


def get(url, **kwargs):
    """
    发送一个Get请求
    :param url: 请求地址
    :param kwargs: body=None, headers=None, token=None.
    :return:
    """
    return send(url, 'get', **kwargs)


def post(url, **kwargs):
    """
    发送一个Get请求
    :param url: 请求地址
    :param kwargs: body=None, headers=None, token=None.
    :return:
    """
    return send(url, 'post', **kwargs)


class ApiRes:

    def __init__(self, response):
        self.response = response
        print(self.err_msg())

    def err_code(self):
        return self.parse_text()['errCode']

    def err_msg(self):
        return self.parse_text()['errMsg']

    def data(self):
        return self.parse_text()['data']

    def parse_text(self):
        return json.loads(self.response.text)

    def is_err(self):
        return self.err_code() == 0
