# coding=utf-8
import datetime
import time

import requests
import model
import config
import json
import threading
import sys
import re
import log
import update_temp

# import update_temp

switch = True
log = log.Log()


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


def get_url(q):
    # 要访问的目标页面
    targetUrl = "http://www.kuaidi100.com/query?type={}&postid={}"
    db = model.Express_by_MS()
    item = db.get_unfinished_random(q)

    urls = []

    for i in item:
        url = targetUrl.format(i[2], i[1])
        urls.append(url)
    return urls


# def save_result(update_time, took_time, confirm_time, last_time, state, item_tag, results, express_order, details):
#     conn = psycopg2.connect(database=PG_DATABASE, user=PG_USERNAME, password=PG_PASSWORD, host=PG_HOST,
#                             port=PG_PORT)
#     cursor = conn.cursor()
#
#     SQL = """UPDATE express SET update_time={}, took_time={},confirm_time={},last_time={},state={},item_tag={},results={}
#                     WHERE express_order='{}';""".format(update_time, took_time, confirm_time, last_time, state,
#                                                         item_tag,
#                                                         results,
#                                                         express_order)
#     cursor.execute(SQL)
#
#     for i in range(len(details)):
#         node_id = express_order + "[" + str(i) + "]"
#
#         SQL = "select node_id from express_details WHERE node_id='{}'".format(node_id)
#         # print(SQL)
#         cursor.execute(SQL)
#         res = cursor.fetchone()
#         if not res:
#             SQL = "INSERT INTO express_details (express_order, node_date,node_content,node_id) VALUES ('{}','{}','{}','{}')".format(
#                 express_order, details[i]['time'], details[i]['context'], node_id)
#             # print(SQL)
#             cursor.execute(SQL)
#
#     conn.commit()
#     cursor.close()
#     conn.close()


def main(i):
    proxies = get_proxies()
    urls = get_url(i)

    if not urls:
        log.critical('已无信息需要爬取')
        global switch
        switch = False

    for url in urls:
        resp = requests.get(url)
        # resp = requests.get(url, proxies=get_proxies())

        express_order = re.findall("\d+", re.search('postid=.*', url).group())[0]

        if resp.status_code == 200:
            result = json.loads(resp.text)
            item = {}
            item['request_flag'] = result['message']
            item['update_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            item['Has_Signed'] = 0
            item['Synchronous'] = 1

            if item['request_flag'] == 'ok':
                item['Process_Status'] = 1
                item['Express_Status'] = result['state']
                item['Express_No'] = result.get('nu', '')
                item['Express_Company'] = result.get('com', '')
                item['content'] = result.get('data', '')[::-1]
                item['latest_content'] = result.get('data', [{"time": "Null", "context": ""}])[0]['context']
                item['latest_tiem'] = result.get('data', [{"time": "Null", "context": ""}])[0]['time']
                if item['Express_Status'] == '3':
                    item['Has_Signed'] = 1
                    item['Process_Status'] = 2


            elif item['request_flag'] == '快递公司参数异常：单号不存在或者已经过期':
                item['Express_Status'] = result['state']
                item['results'] = '快递公司参数异常：单号不存在或者已经过期'
                item['Express_No'] = express_order
                item['Process_Status'] = 1

            db = model.Express_by_MS()
            db.save_result(item)

            log.info('抓取单号信息完成:' + str(express_order))
            time.sleep(1)

        else:
            log.error('请求失败，状态码：', resp.status_code)


if __name__ == '__main__':

    c = 0

    update_temp.update()

    while switch:

        db = model.Express_by_MS()
        db.init_get_unfinished_random()

        c += 1

        if c > 10:
            update_temp.update()
            update_temp.push()
            c = 0

        my_thread = []

        thread_count = 2  # 调用 thread_count 个线程
        parse = 5  # 一个线程解析 parse 个url

        for i in range(thread_count):
            t = threading.Thread(target=main, args=(parse,))
            my_thread.append(t)

        for i in range(thread_count):
            my_thread[i].start()
            time.sleep(1)

        for i in range(thread_count):
            my_thread[i].join()
            time.sleep(1)

        time.sleep(10)
