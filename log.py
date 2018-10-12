# coding=utf-8
import logging  # 引入logging模块


class Log:

    def __init__(self):
        # 第一步，创建一个logger
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)  # Log等级总开关
        # 第二步，创建一个handler，用于写入日志文件
        logfile = 'log.txt'
        fh = logging.FileHandler(logfile, mode='a')
        fh.setLevel(logging.DEBUG)  # 输出到file的log等级的开关
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')  # logging.basicConfig函数对日志的输出格式及方式做相关配置
        # 第三步，定义handler的输出格式
        formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
        fh.setFormatter(formatter)

        # 第四步，将logger添加到handler里面
        self.logger.addHandler(fh)

    def debug(self, content):
        self.logger.debug(content)

    def info(self, content):
        self.logger.info(content)

    def warning(self, content):
        self.logger.warning(content)

    def error(self, content):
        self.logger.error(content)

    def critical(self, content):
        self.logger.critical(content)
