# coding=utf-8
import datetime
import time
import requests
import json
import model


def baidu(target, proxies):
    """
    :param target: target[1] 快递公司, target[0] 快递单号
    :param proxies: 代理
    :return:
    """
    url = "https://sp0.baidu.com/9_Q4sjW91Qh3otqbppnN2DJv/pae/channel/data/asyncqury?appid=4001&com=&nu={}".format(
        target[0])

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'Cookie': 'BAIDUID=:FG=; BIDUPSID=; PSTM=; delPer=0'
    }

    if proxies == 0:
        resp = requests.get(url=url, headers=headers)
    else:
        resp = requests.get(url=url, headers=headers, proxies=proxies)

    result = json.loads(eval("u'%s'" % resp.text))
    item = {}
    if result['status'] == '-5':
        item['Express_Status'] = 0
        item['results'] = '单号暂无物流进展'
        item['Express_No'] = target[0]
        item['Process_Status'] = 1
        return item

    if result['status'] == '-2':
        item['Express_Status'] = 0
        item['results'] = '单号错误'
        item['Express_No'] = target[0]
        item['Process_Status'] = 1
        return item

    if result['status'] == '0':

        item['request_flag'] = 'ok'
        item['update_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        item['Has_Signed'] = 0
        item['Synchronous'] = 1

        item['Process_Status'] = 1
        item['Express_Status'] = result['data']['info']['state']
        item['Express_No'] = target[0]
        item['Express_Company'] = result['data']['info']['com']
        item['content'] = []
        temp = result['data']['info']['context'][::-1]
        for i in range(len(temp)):
            t = temp[i]['time']
            time_local = time.localtime(int(t))
            strtime = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
            d = {
                'context': temp[i]['desc'],
                'time': strtime
            }
            item['content'].append(d)

        item['latest_content'] = item['content'][-1]['context']
        item['latest_tiem'] = item['content'][-1]['time']
        if item['Express_Status'] == '3':
            item['Has_Signed'] = 1
            item['Process_Status'] = 2

    return item


def kuaidi100(target, proxies):
    """
    :param target: target[1] 快递公司, target[0] 快递单号
    :param proxies: 代理
    :return:
    """
    url = "http://www.kuaidi100.com/query?type={}&postid={}".format(target[1], target[0])

    if proxies == 0:
        resp = requests.get(url=url)
    else:
        resp = requests.get(url=url, proxies=proxies)

    item = {}

    if resp.status_code == 200:
        result = json.loads(resp.text)

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
            item['Express_No'] = target[0]
            item['Process_Status'] = 1

    return item


def ckd8(target, proxies):
    """
    :param target: target[1] 快递公司, target[0] 快递单号
    :param proxies: 代理
    :return:
    """
    url = 'https://www.ckd8.com/open.php'
    data = "express={}&number={}&nu=&op=open&tp=0".format(target[1], target[0])
    headers = {
        'Host': 'www.ckd8.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0',
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://www.ckd8.com/{}/?wd={}'.format(target[1], target[0]),
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Requested-With': 'XMLHttpRequest',

    }

    item = {}
    if proxies == 0:
        resp = requests.post(url=url, data=data, headers=headers)
    else:
        resp = requests.post(url=url, data=data, headers=headers, proxies=proxies)

    if resp.status_code == 200:
        result = json.loads(resp.text)
        if result['status'] == '4':
            item['Express_Status'] = 0
            item['results'] = '输入的单号正确'
            item['Express_No'] = target[0]
            item['Process_Status'] = 1
            return item

        if result['status'] == '0':
            item['Express_Status'] = 0
            item['results'] = '暂无跟踪信息'
            item['Express_No'] = target[0]
            item['Process_Status'] = 1
            return item

        if result['status'] == '1':

            item['request_flag'] = 'ok'
            item['update_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            item['Has_Signed'] = 0
            item['Synchronous'] = 1

            item['Process_Status'] = 1
            item['Express_Status'] = result['state']
            item['Express_No'] = target[0]
            item['Express_Company'] = target[1]
            item['content'] = []
            temp = result['data']
            for i in range(len(temp)):
                t = temp[i]['time']
                time_local = time.localtime(int(t))
                strtime = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
                d = {
                    'context': temp[i]['context'],
                    'time': strtime
                }
                item['content'].append(d)

            item['latest_content'] = item['content'][-1]['context']
            item['latest_tiem'] = item['content'][-1]['time']
            if item['Express_Status'] == '3':
                item['Has_Signed'] = 1
                item['Process_Status'] = 2

    return item


if __name__ == '__main__':
    n = ckd8(('3102043855170', 'yunda'), 0)
    print(n)