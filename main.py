# coding=utf-8
import datetime
import time

import requests
import model
import config
import psycopg2
import json
import threading
import sys
import re
import log

PG_USERNAME = 'smallpot'
PG_PASSWORD = 'yj'
PG_HOST = '58.63.214.44'
PG_PORT = '5432'
PG_DATABASE = 'express_spider'

switch = True
log = log.Log()

result_state = {
    '0': '在途',
    '1': '揽件',
    '2': '疑难',
    '3': '签收',
    '4': '退签',
    '5': '派件',
    '6': '退回',
}


def get_proxies():
    # 代理服务器
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


# resp = requests.get(targetUrl, proxies=get_proxies())
#
# print(resp.status_code)
# print(resp.text)

def get_url(q):
    # 要访问的目标页面
    targetUrl = "http://www.kuaidi100.com/query?type={}&postid={}"
    db = model.Express()
    item = db.get_unfinished_random(q)

    urls = []

    for i in item:
        url = targetUrl.format(i[3], i[2])
        urls.append(url)

    return urls


def save_result(update_time, took_time, confirm_time, last_time, state, item_tag, results, express_order):
    conn = psycopg2.connect(database=PG_DATABASE, user=PG_USERNAME, password=PG_PASSWORD, host=PG_HOST,
                            port=PG_PORT)
    cursor = conn.cursor()

    SQL = """UPDATE express SET update_time={}, took_time={},confirm_time={},last_time={},state={},item_tag={},results={}
                    WHERE express_order={};""".format(update_time, took_time, confirm_time, last_time, state, item_tag,
                                                      results,
                                                      express_order)

    cursor.execute(SQL)
    conn.commit()
    cursor.close()
    conn.close()


def main(i):
    proxies = get_proxies()
    urls = get_url(i)




    if not urls:
        log.critical('已无信息需要爬取')
        global switch
        switch = False

    for url in urls:
        resp = requests.get(url, proxies=get_proxies())

        express_order = re.findall("\d+", re.search('postid=.*', url).group())[0]

        if resp.status_code == 200:
            result = json.loads(resp.text)
            item = {}
            item['item_tag'] = result['message']
            if item['item_tag'] == 'ok':
                item['state'] = result_state[result['state']]
                item['last_time'] = result.get('data', [''])[0]['time']
                item['took_time'] = result.get('data', [''])[-1]['time']
                item['results'] = result.get('data', [''])[0]['context']
                item['express_order'] = result.get('nu', '')
                item['update_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                if item['state'] == '签收':
                    item['confirm_time'] = result.get('data', None)[-1]['time']
                else:
                    item['confirm_time'] = ''

            elif item['item_tag'] =='快递公司参数异常：单号不存在或者已经过期':
                item['state'] = result_state[result['state']]
                item['results']='快递公司参数异常：单号不存在或者已经过期'
                item['express_order'] = express_order
                item['update_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                item['item_tag'] = "ok"

                took_time = "'" + item.get('took_time') + "'" if item.get('took_time') else 'Null'
                confirm_time = "'" + item.get('confirm_time') + "'" if item.get('confirm_time') else 'Null'
                last_time = "'" + item.get('last_time') + "'" if item.get('last_time') else 'Null'
                update_time = "'" + item.get('update_time') + "'" if item.get('update_time') else 'Null'
                state = "'" + item.get('state') + "'"
                results = "'" + item.get('results') + "'"
                item_tag = "'" + item.get('item_tag') + "'"
                express_order = "'" + item.get('express_order') + "'"

                save_result(took_time=took_time, confirm_time=confirm_time, last_time=last_time,
                            update_time=update_time, state=state, results=results, item_tag=item_tag,
                            express_order=express_order)

                log.info('抓取单号信息完成:', express_order)
                time.sleep(1)

        else:
            log.error('请求失败，状态码：', resp.status_code)


if __name__ == '__main__':

    c = 0
    while switch:

        c += 1

        log.info("*******进行第" + str(c) + "轮抓取*******")

        my_thread = []

        thread_count = 2  # 调用 thread_count 个线程
        parse = 20  # 一个线程解析 parse 个url

        for i in range(thread_count):
            t = threading.Thread(target=main, args=(parse,))
            my_thread.append(t)

        for i in range(thread_count):
            my_thread[i].start()
            time.sleep(1)

        for i in range(thread_count):
            my_thread[i].join()
            time.sleep(1)

        time.sleep(5)
