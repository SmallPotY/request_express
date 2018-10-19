# coding=utf-8

import logging
import getpass
import sys


# 定义Mylog类，管理log信息
class MyLog:
    def __init__(self):
        self.user = getpass.getuser()
        self.logger = logging.getLogger(self.user)
        self.logger.setLevel(logging.DEBUG)

        # 日志文件名
        self.logFile = sys.argv[0][0:-3] + '.log'
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
        self.formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")

        # 日志显示到屏幕并输出到文档
        self.logHand = logging.FileHandler(self.logFile, encoding='utf-8')
        self.logHand.setFormatter(self.formatter)
        self.logHand.setLevel(logging.DEBUG)

        self.logHandSt = logging.StreamHandler()
        self.logHandSt.setFormatter(self.formatter)
        self.logHandSt.setLevel(logging.DEBUG)

        self.logger.addHandler(self.logHand)
        self.logger.addHandler(self.logHandSt)

        #  用pop方法把logger.handlers列表中的handler移除，解决多模块引用重复输出的问题，注意如果你add了多个handler，这里需多次pop，或者可以直接为handlers列表赋空值
        self.logger.handlers.pop()
        # self.logger.handler = []

    # 日志的5个级别对应5个函数
    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warn(self, msg):
        self.logger.warn(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)


# 测试代码 __name__是访问当前函数名的方法，如果作为模块就不是main函数 下面的方法不会执行
if __name__ == '__main__':
    mylog = MyLog()
    mylog.debug("fffff")
    mylog.info("I;m info")
    mylog.warn("warning")
    mylog.error("Error")
    mylog.critical("this is a critical")
