# coding=utf-8
import pymssql
import datetime
from config import DB_token
import helper
from main import log



class Express_by_Tiantu:

    def __init__(self):
        self.conn = pymssql.connect(server=DB_token['tiantu']['MS_server'], port=DB_token['tiantu']['MS_port'],
                                    user=DB_token['tiantu']['MS_user'], password=DB_token['tiantu']['MS_password'],
                                    database=DB_token['tiantu']['MS_database'], charset='UTF-8')

    def push_update(self, item):
        # print(item)
        cursor = self.conn.cursor()
        sql = "INSERT INTO Express_Trace_Temp (Express_No,Express_Company,Express_Status,Has_Signed,Trace_Context,Trace_Date_Time,Process_Status) VALUES {}".format(
            item)
        # print(sql)
        try:
            cursor.execute(sql)
        except:
            log.error('执行SQL错误,代号[push_update_001],错误语句：' + str(sql))
        self.conn.commit()
        self.conn.close()


class Express_by_MS:

    def __init__(self):
        self.conn = pymssql.connect(server=DB_token['MSSQL']['MS_server'], port=DB_token['MSSQL']['MS_port'],
                                    user=DB_token['MSSQL']['MS_user'], password=DB_token['MSSQL']['MS_password'],
                                    database=DB_token['MSSQL']['MS_database'], charset='UTF-8')

    def get_temp_express(self, q):
        """
        将临时表中的快递单号存入查询表中
        :return:
        """
        cursor = self.conn.cursor()
        sql = """
            SELECT TOP {} Express_No,Express_Company,id FROM express_temp WHERE Process_Status=0
            """.format(q)
        cursor.execute(sql)
        rows = cursor.fetchall()
        conditions = tuple(i[2] for i in rows)
        if conditions:
            if len(conditions) < 2:
                sql = "UPDATE express_temp SET Process_Status=1 WHERE id = {}".format(conditions[0])
            else:
                sql = "UPDATE express_temp SET Process_Status=1 WHERE id in {}".format(conditions)
            cursor.execute(sql)
        self.conn.commit()

        for i in rows:
            # 不存在记录插入，存在则将记录变更为未查询状态状态
            sql = """      
                IF EXISTS(SELECT Express_No FROM express WHERE Express_No = '{Express_No}')
                BEGIN
                UPDATE express SET Process_Status = 0 WHERE Express_No = '{Express_No}'
                END
                ELSE
                BEGIN
                INSERT INTO express (Express_No,Express_Company) VALUES('{Express_No}', '{Express_Company}')
                END
            """.format(Express_No=i[0], Express_Company=i[1])
            cursor.execute(sql)
        self.conn.commit()
        self.conn.close()
        # print("更新快递查询池完成")

    def get_unfinished_random(self, q):
        cursor = self.conn.cursor()
        sql = "SELECT top {} * FROM express WHERE Process_Status=0 AND query_ongoing=0  ORDER BY newid()".format(q)
        cursor.execute(sql)
        rows = cursor.fetchall()
        result = [i for i in rows]
        conditions = tuple([i[0] for i in rows])
        if conditions:
            if len(conditions) < 2:
                sql = "UPDATE express SET query_ongoing=1 WHERE id = {}".format(conditions[0])
            else:
                sql = "UPDATE express SET query_ongoing=1 WHERE id in {}".format(conditions)
            cursor.execute(sql)
            self.conn.commit()
        self.conn.close()
        return result

    def init_get_unfinished_random(self):
        cursor = self.conn.cursor()
        sql = "UPDATE express SET query_ongoing=0"
        cursor.execute(sql)
        self.conn.commit()
        self.conn.close()

    def save_result(self, item):
        """
        更新查询信息
        :param item:
        :return:
        """
        # print(item)

        cursor = self.conn.cursor()

        Process_Status = item.get('Process_Status',-1)  # 查询标识
        Express_Status = item.get('Express_Status',-1)  # 快递状态
        Has_Signed = item.get('Has_Signed',-1)  # 是否签收
        update_time = item.get('update_time','1999-01-01 0:00:00')  # 更新时间
        request_flag = item.get('request_flag')  # 请求结果
        latest_content = item.get('latest_content')  # 最后状态
        latest_tiem = item.get('latest_tiem','1999-01-01 0:00:00')  # 最后时间
        Express_No = item.get('Express_No')  # 单号

        sql = """
                UPDATE express SET Process_Status='{Process_Status}',Express_Status='{Express_Status}',
                Has_Signed='{Has_Signed}',update_time='{update_time}',request_flag='{request_flag}',latest_content='{latest_content}',latest_tiem='{latest_tiem}'
                WHERE Express_No='{Express_No}'
        """.format(Process_Status=Process_Status, Express_Status=Express_Status, Has_Signed=Has_Signed,
                   update_time=update_time, request_flag=request_flag, latest_content=latest_content,
                   latest_tiem=latest_tiem, Express_No=Express_No)

        # print(sql)
        try:
            cursor.execute(sql)
        except:
            log.error('执行SQL错误,代号[001],传入item：' + str(item) + '[SQL]:'+sql)

        sql = "UPDATE express_temp SET Process_Status=2 WHERE Express_No='{}'".format(Express_No)
        try:
            cursor.execute(sql)
        except:
            log.error('执行SQL错误,代号[002],传入item：' + str(item))

        if item.get('content'):
            for i in range(len(item.get('content'))):
                trace_flag = Express_No + "-[" + str(i) + "]"
                sql = "select Trace_flag from express_info WHERE Trace_flag='{}'".format(trace_flag)
                cursor.execute(sql)
                res = cursor.fetchone()
                if not res:
                    phase = '未知'
                    t = helper.judge_phase(item['content'][i]['context'])
                    if t[0]:
                        if t[0] ==1 :
                            phase = t[1]
                        else:
                            phase = '，'.join(t[1])
                    sql = "INSERT INTO express_info (Express_No, Trace_Context,Trace_Date_Time,Trace_flag,Trace_serial,Trace_Phase) VALUES ('{}','{}','{}','{}','{}','{}')".format(
                        Express_No, item['content'][i]['context'], item['content'][i]['time'], trace_flag, i,phase)
                    try:
                        cursor.execute(sql)
                    except:
                        log.error('执行SQL错误,代号[003],传入item：' + str(item))

        self.conn.commit()
        self.conn.close()

    def get_push(self):
        cursor = self.conn.cursor()
        sql = """
                SELECT i.Express_No,e.Express_Company,e.Express_Status,e.Has_Signed,i.Trace_Context,i.Trace_Date_Time FROM express_info i
                left  JOIN  express e ON i.Express_No=e.Express_No
                WHERE i.Synchronous=1
                UPDATE express_info SET Synchronous=0
                """
        cursor.execute(sql)
        rows = cursor.fetchall()
        result = [str((i[0], i[1], i[2], i[3], i[4], i[5].strftime('%Y-%m-%d %H:%M:%S'), '0')) for i in rows]
        # print(result)
        result = ','.join([str(i) for i in result])

        self.conn.commit()
        self.conn.close()
        return result


if __name__ == '__main__':
    db = Express_by_MS()

    db.conn.commit()