from configparser import ConfigParser

config = ConfigParser()
setting_file = 'config.ini'


def red_config(sections):
    config.read(setting_file, 'utf-8')
    return config[sections]


class Base:

    @staticmethod
    def output():
        return red_config('Base')['output']

    @staticmethod
    def log():
        return red_config('Base')['log']


class Api:
    @staticmethod
    def ws_url():
        return red_config('Api')['ws_url']

    @staticmethod
    def user_register():
        return red_config('Api')['user_register']

    @staticmethod
    def user_token():
        return red_config('Api')['user_token']

    @staticmethod
    def user_login():
        return red_config('Api')['user_login']

    @staticmethod
    def msg_send():
        return red_config('Api')['msg_send']


class Reliability:

    @staticmethod
    def user_from():
        return red_config('Reliability')['user_from']

    @staticmethod
    def user_to():
        return red_config('Reliability')['user_to']
