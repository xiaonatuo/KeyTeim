import json
import threading
import time
import uuid

from numpy import *

from common import settings
from core.user import User


def get_user_from():
    """
    读取配置文件中的发送消息的用户信息，并创建用户对象

    Return:
        用户对象
    """
    from_str = settings.Reliability.user_from()
    from_arr = from_str.split('::')
    return User(user_id=from_arr[0], pwd=from_arr[1])


def get_user_to():
    """
    读取配置文件中的接收消息的用户信息，并创建用户对象

    Return:
        用户对象
    """
    to_str = settings.Reliability.user_to()
    to_arr = to_str.split('::')
    return User(user_id=to_arr[0], pwd=to_arr[1])


def build_samples():
    """
    构建消息测试样本数据

    Return:
        消息样本数据列表
    """
    samples_nums = int(settings.Base.samples_nums())
    __samples_list = []
    index = 0
    while index < samples_nums:
        __samples_list.append(Samples(f'测试样本消息-{index}'))
        index += 1
    return __samples_list


# 消息样本缓存
samples_cache = {}
# 消息发送间隔
msg_send_interval = int(settings.Base.msg_send_interval()) / 1000
# 消息接收超时时间
msg_recv_timeout = int(settings.Base.msg_recv_timeout()) / 1000
# 登录超时时间
login_timeout = int(settings.Base.login_timeout()) / 1000

# 登录回调函数锁
login_callback_lock = threading.Lock()


class Tester:

    def __init__(self):
        self.samples = None
        self.__user_from = None
        self.__user_to = None
        self.__client_nums = 2
        self.__begin_time = None
        self.__exit = False

    def start(self):
        self.__begin_time = time.time()
        # 生成样本数据
        self.samples = build_samples()

        # 获取并生成用户信息
        self.__user_from = get_user_from()
        self.__user_to = get_user_to()
        # 绑定收到消息回调函数
        self.__user_to.on_msg = self.__parse_msg

        # 绑定登录成功回调函数
        self.__user_from.login_callback = self.__login_callback
        self.__user_to.login_callback = self.__login_callback

        # 登录
        threading.Thread(self.__user_from.login()).start()
        threading.Thread(self.__user_to.login()).start()

        # 监听登录状态，超时退出脚本
        time_flag = time.time()
        while self.__client_nums > 0:
            time.sleep(0.01)
            if time.time() - time_flag > login_timeout:
                print('错误：用户登录超时')
                exit(1)

        # 程序退出判断
        while not self.__exit:
            time.sleep(1)

    def __send_samples(self):
        print(f'\n---------- 开始发送消息样本 ----------\n')
        for samples in self.samples:
            time.sleep(msg_send_interval)
            samples.send_time = time.time()
            self.__user_from.send_text_message(self.__user_to.user_id, samples.to_str())
            samples_cache[samples.id] = samples

        print(f'\n---------- 所有样本发送完毕 ----------\n')
        # 开始分析样本
        threading.Thread(target=self.__analyze_samples).start()

    def __login_callback(self):
        """
        登录成功的回调函数，每调用一次对 client_nums 进行减1操作，为0时，执行发送样本数据
        """
        # 加锁保证该方法只能由一个线程执行
        login_callback_lock.acquire()
        self.__client_nums -= 1
        if self.__client_nums == 0:
            threading.Thread(target=self.__send_samples).start()
        # 释放锁
        login_callback_lock.release()

    def __parse_msg(self, msg_samples):
        """
        解析样本数据，并设置接收时间
        """
        _samples = json.loads(msg_samples)
        for samples in self.samples:
            if samples.id == _samples['id']:
                samples.recv_time = time.time()
                samples.recv_delay = samples.recv_time - samples.send_time
                samples_cache.pop(samples.id)
                print(f'recv<<<<<<【{self.__user_to.user_id}】接收到了一条消息：{samples.to_str()}')

    def __analyze_samples(self):
        # 所有样本发送完毕，判断待接收的消息缓存中是否还有待接收的消息，
        # 如果有则等待接收消息，若超过消息接收超时时间则直接进行计算结果
        while len(samples_cache) > 0:
            values = samples_cache.values()
            times = []
            for val in values:
                times.append(val.send_time)
            timeout = max(times)
            if timeout + msg_recv_timeout < time.time():
                break
            # 休眠10毫秒
            time.sleep(0.01)

        print('\n----------【开始分析样本】----------')
        send_times = []
        recv_times = []
        delay_times = []
        for samples in self.samples:
            if samples.send_time is not None:
                send_times.append(samples.send_time)
            if samples.recv_time is not None:
                recv_times.append(samples.recv_time)
            if samples.recv_delay != -1:
                delay_times.append(samples.recv_delay)

        print(f'发送的样本数：{len(send_times)}')
        print(f'接收的样本数：{len(recv_times)}')
        print(f'丢失的样本数：{len(send_times) - len(recv_times)}')
        print(f'消息送达率：{len(recv_times) / len(send_times) * 100}%')
        print(f'消息接收最大延迟：{format(max(delay_times), ".3f")} 毫秒')
        print(f'消息接收最小延迟：{format(min(delay_times), ".3f")} 毫秒')
        print(f'消息接收平均延迟：{format(mean(delay_times), ".3f")} 毫秒')
        print(f'测试总耗时：{format(time.time() - self.__begin_time, ".3f")} 秒')
        self.__user_from.logout()
        self.__user_to.logout()
        self.__exit = True


class Samples:
    """
    消息样本
    """
    def __init__(self, text):
        """
        Parameters:
            id: 样本ID
            text: 消息文本内容
            create_time: 样本创建时间
            send_time: 样本发送时间
            recv_time: 样本接收时间
            recv_delay: 样本接收延迟
        """
        self.id = str(uuid.uuid3(namespace=uuid.NAMESPACE_DNS, name=text))
        self.text = text
        self.create_time = time.time()
        self.send_time = None
        self.recv_time = None
        self.recv_delay = -1

    def to_str(self):
        return json.dumps({
            'id': self.id,
            'text': self.text,
            'create_time': self.create_time,
            'send_time': self.send_time,
            'recv_time': self.recv_time
        })


if __name__ == '__main__':
    Tester().start()
