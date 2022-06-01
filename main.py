from core.user import User

# 用户登录
from common import settings


def login():
    from_str = settings.Reliability.user_from()
    from_arr = from_str.split('::')
    user = User(user_id=from_arr[0], pwd=from_arr[1])
    user.login()
    print('login done')


# 发送消息
def send_msg():
    print('sendMsg')


# 计算结果
def scal():
    print('scal')


if __name__ == '__main__':
    login()
