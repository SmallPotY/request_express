# coding=utf-8

import model
import datetime
import config


def update(q):
    db = model.Express_by_MS()
    db.get_temp_express(q)
    print(datetime.datetime.now(), "更新快递查询池")


def push():
    db = model.Express_by_MS()
    item = db.get_push()

    # print(item)
    if item:
        tiantu = model.Express_by_Tiantu()
        tiantu.push_update(item)
        print(datetime.datetime.now(), '推送单号信息')
    else:
        print(datetime.datetime.now(),"暂无需要推送的数据")


def update_rootless():
    db = model.Express_by_MS()
    db.repeat_err()
    print(datetime.datetime.now(),'更新查询失败的运单信息')


def update_err_ord():
    db = model.Express_by_MS()
    db.repeat_rootless()
    print(datetime.datetime.now(),'更新未有揽收状态的运单信息')


def update_config():
    db = model.Express_by_MS()
    result = db.loading_config()
    config.query_interval = result['query_interval']
    config.query_first_interval = result['query_first_interval']
    config.thread_nbmber = result['thread_nbmber']
    config.parse_nbmber = result['parse_nbmber']
    config.query_err_interval = result['query_err_interval']
    print('****本轮配置信息****')
    print(
        '已揽收更新间隔[{query_interval}]-未揽收更新间隔[{query_first_interval}]-查询失败更新间隔[{query_err_interval}]-开启线程[{thread_nbmber}]-每线程查询数[{parse_nbmber}]'.format(
            query_interval=result['query_interval'],
            query_first_interval=result['query_first_interval'],
            query_err_interval=result['query_err_interval'],
            thread_nbmber=result['thread_nbmber'],
            parse_nbmber=result['parse_nbmber']))
