import pymssql
import threading
import time
from config import DB_token
from log import MyLog

log = MyLog()


def judge_phase(content):
    guess = []

    key_state = {
        '打包': '途中',
        '发出': '途中',
        '收入': '途中',
        '发往': '途中',
        '到达': '途中',
        '到件扫描': '途中',
        '称重扫描': '途中',
        '进行分拨': '途中',
        '【反馈】扫描': '途中',
        '离开': '途中',
        '卸车扫描': '途中',
        '【称重】扫描': '途中',
        '【到件】扫描': '途中',
        '【卸车】扫描': '途中',
        '【分发】扫描': '途中',
        '快件扫描': '途中',
        '已拆包': '途中',
        '已收寄': '途中',
        '签收': '签收',
        '代收': '签收',
        '为您服务': '签收',
        '派件': '派件',
        '【派送】扫描': '派件',
        '收件': '揽收',
        '揽收': '揽收',
        '揽件': '揽收',
        '揽件扫描': '揽收',
        '问题件': '问题件'
    }

    for k, v in key_state.items():
        if k in content:
            guess.append(v)

    result = set(guess)
    situation = len(result)

    if situation == 1:
        # log.debug('成功=>' + content + '=>' + guess[0])
        return (1, guess[0])

    if situation > 1:
        if '已签收' in content:
            log.debug('歧义=>' + content + '=>' + '签收')
            return (1, '签收')
        if '代收' in content and '取件' in content:
            log.debug('歧义=>' + content + '=>' + '签收')
            return (1, '签收')
        if '途中' in guess and '收件' in guess:
            log.debug('歧义=>' + content + '=>' + '途中')
            return (1, '途中')
        if '途中' in guess and '签收' in guess:
            log.debug('歧义=>' + content + '=>' + '签收')
            return (1, '签收')
        if '已被' in guess and '代签收' in content:
            log.debug('歧义=>' + content + '=>' + '签收')
            return (1, '签收')
        if '派件' in content and '代收' in content:
            log.debug('歧义=>' + content + '=>' + '代收')
            return (1, '代收')

        if '正在进行扫描' in content:
            log.debug('歧义=>' + content + '=>' + '途中')
            return (1, '途中')

        log.debug('歧义=>分析失败=>' + content + '=>' + ','.join(result))
        return (2, result, content)
    if situation == 0:
        log.debug('失败=>' + content)
        return (0, content)


class Express_by_MS:

    def __init__(self):
        self.conn = pymssql.connect(server=DB_token['MSSQL']['MS_server'], port=DB_token['MSSQL']['MS_port'],
                                    user=DB_token['MSSQL']['MS_user'], password=DB_token['MSSQL']['MS_password'],
                                    database=DB_token['MSSQL']['MS_database'], charset='UTF-8')

    def test(self):
        cursor = self.conn.cursor()

        sql = "SELECT id,Trace_Context FROM express_info where Trace_Phase='未知'"

        cursor.execute(sql)
        rows = cursor.fetchall()
        self.conn.close()
        return rows

    def r(self, NEW, ID):
        cursor = self.conn.cursor()
        sql = "UPDATE  express_info SET Trace_Phase = '{}' WHERE ID = '{}'".format(NEW, ID)

        cursor.execute(sql)
        self.conn.commit()
        self.conn.close()


def save(i):
    new_content = judge_phase(i[1])
    db = Express_by_MS()
    if new_content[0] == 1:
        db.r(new_content[1], i[0])
    if new_content[0] == 2:
        db.r(','.join(new_content[1]), i[0])
    if new_content[0] == 0:
        db.r('未知', i[0])


if __name__ == '__main__':

    db = Express_by_MS()
    rows = db.test()

    p = []
    my_thread = []

    for i in rows:
        p.append(i)


    for i in range(len(p)):
        t = threading.Thread(target=save, args=(p[i],))
        my_thread.append(t)



    for i in range(len(p)):
        my_thread[i].start()


    for i in range(len(p)):
        my_thread[i].join()

