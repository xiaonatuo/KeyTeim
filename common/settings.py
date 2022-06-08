from configparser import ConfigParser

config = ConfigParser()
setting_file = 'config.ini'


def red_config(sections):
    config.read(setting_file, 'utf-8')
    return config[sections]


class Base:

    @staticmethod
    def login_timeout():
        """
        登录超时时间（单位：毫秒）
        """
        return red_config('Base')['login_timeout']

    @staticmethod
    def samples_nums():
        """
        发送测试样本的数量
        """
        return red_config('Base')['samples_nums']

    @staticmethod
    def msg_send_interval():
        """
        消息发送时间间隔（单位：毫秒）
        """
        return red_config('Base')['msg_send_interval']

    @staticmethod
    def msg_recv_timeout():
        """
        消息接收超时时间(单位：毫秒)
        """
        return red_config('Base')['msg_recv_timeout']


class Api:
    @staticmethod
    def ws_url():
        return red_config('Api')['ws_url']

    @staticmethod
    def user_token():
        return red_config('Api')['user_token']


class Reliability:

    @staticmethod
    def user_from():
        return red_config('Reliability')['user_from']

    @staticmethod
    def user_to():
        return red_config('Reliability')['user_to']
