# coding=utf-8
import datetime
import time
import random
import requests
import model
import config
import json
import threading
import sys
import re
from log import MyLog
import update_temp
import api as api_choose

switch = True
log = MyLog()


api_free = [api_choose.baidu, api_choose.kuaidi100, api_choose.ckd8]
api_pay = [api_choose.showapi]


get_temp = 100  # 每次从临时表提取记录数
L = threading.Lock()    # 引入锁

def get_proxies():
    """
    :return: 阿布云HTTP代理隧道
    """
    proxyHost = config.proxyHost
    proxyPort = config.proxyPort
    proxyUser = config.proxyUser
    proxyPass = config.proxyPass
    proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
        "host": proxyHost,
        "port": proxyPort,
        "user": proxyUser,
        "pass": proxyPass,
    }
    proxies = {
        "http": proxyMeta,
        "https": proxyMeta,
    }
    return proxies


def get_target(q):
    """
    :param q: 获取的记录数
    :return: 随机获取 q 条快递记录，[('#快递单号','#快递公司','#最近一次查询状态'),('#快递单号','#快递公司','#最近一次查询状态')]
    """
    db = model.Express_by_MS()
    item = db.get_unfinished_random(q)
    targets = []
    for i in item:
        targets.append((i[1], i[2], i[7]))
    return targets


def parsing(api, target, proxies):
    """
    :param api:调用的api，从全局的api_list中随机选取
    :param target:元组：(#快递单号,#快递公司)
    :param proxies:指定代理,传入 0 不使用代理
    :return:返回查询结果
    """
    if proxies == 0:
        return api(target, 0)
    else:
        return api(target, proxies)


def main(i):
    proxies = get_proxies()
    targets = get_target(i)  # 获取i个单号

    if not targets:
        log.critical('已无信息需要爬取,重新推送未签收数据')

        db = model.Express_by_MS()
        db.repeat()
        time.sleep(5)
        global switch
        switch = False

    switch = True

    for i in targets:

        if i[2]:
            if i[2] == 'ok':
                # 上一次查询失败调用付费接口
                api = random.choice(api_free)
            else:
                api = random.choice(api_pay)

        else:
            # 第一次查询用免费接口
            api = random.choice(api_free)


        L.acquire() # 加锁

        item = parsing(api, i, proxies)
        db = model.Express_by_MS()
        db.save_result(item)
        log.info('通过【' + api.__name__ + '】抓取单号完成=>' + str(i[0]))

        L.release() # 放锁




if __name__ == '__main__':

    update_temp.update(get_temp)


    while switch:

        db = model.Express_by_MS()
        db.init_get_unfinished_random()

        my_thread = []

        thread_count = config.thread_nbmber  # 调用 thread_count 个线程
        parse = config.parse_nbmber  # 一个线程解析 parse 个url

        for i in range(thread_count):
            t = threading.Thread(target=main, args=(parse,))
            my_thread.append(t)

        for i in range(thread_count):
            my_thread[i].start()
            time.sleep(1)

        for i in range(thread_count):
            my_thread[i].join()
            time.sleep(1)

        time.sleep(2)

        update_temp.update(get_temp)
        update_temp.push()
        update_temp.update_rootless()
        update_temp.update_rootless()
        update_temp.update_config()

        print('.........')
        time.sleep(4)
