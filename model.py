# coding=utf-8
import datetime
import json
import helper
import pymssql
from config import DB_token
from  main import log
# from log import logging as log
import sys
import os



class Express_by_Tiantu:

    def __init__(self):
        self.conn = pymssql.connect(server=DB_token['tiantu']['MS_server'], port=DB_token['tiantu']['MS_port'],
                                    user=DB_token['tiantu']['MS_user'], password=DB_token['tiantu']['MS_password'],
                                    database=DB_token['tiantu']['MS_database'], charset='UTF-8')

    def push_update(self, item):
        # print(item)

        cursor = self.conn.cursor()
        sql = "INSERT INTO Express_Trace_Temp (Express_No,Express_Company,Express_Status,Has_Signed,Trace_Context,Trace_Date_Time,Process_Status,Trace_phase) VALUES {}".format(
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
        """

        :rtype: object
        """
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
        sql = "SELECT top {} * FROM express WHERE Process_Status=0 AND query_ongoing=0 AND  query_disably<>1 ORDER BY newid()".format(q)
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
        :param item:保存的item
        :return:
        """
        # print(item)
        cursor = self.conn.cursor()

        request_flag = item.get('request_flag')  # 请求结果

        if request_flag=='ok':
            Process_Status = item.get('Process_Status')  # 查询标识
            Express_Status = item.get('Express_Status')  # 快递状态
            Has_Signed = item.get('Has_Signed')  # 是否签收
            update_time = item.get('update_time')  # 更新时间
            latest_content = item.get('latest_content')  # 最后状态
            latest_tiem = item.get('latest_tiem')  # 最后时间
            Express_No = item.get('Express_No')  # 单号
            # query_disably = item.get('query_disably',0) # 是否不用查询了
        
            sql = """UPDATE express SET Process_Status='{Process_Status}',Express_Status='{Express_Status}',err_count='0',
                    Has_Signed='{Has_Signed}',update_time='{update_time}',request_flag='{request_flag}',latest_content='{latest_content}',latest_tiem='{latest_tiem}'
                    WHERE Express_No='{Express_No}';
                    UPDATE express_temp SET Process_Status=2 WHERE Express_No='{Express_No}'
                    """.format(Process_Status=Process_Status, Express_Status=Express_Status, Has_Signed=Has_Signed,
                    update_time=update_time, request_flag=request_flag, latest_content=latest_content,
                    latest_tiem=latest_tiem, Express_No=Express_No)
            # print(sql)
            try:
                cursor.execute(sql)
                self.conn.commit()
            except:
                log.error('执行save_result错误,代号[001],传入item：' + str(item) + '[SQL]:'+sql)
            finally:
                pass             

        else:
            Express_No = item.get('Express_No')  # 单号
            sql ="select err_count,Note from express where Express_No='{}'".format(Express_No)
            cursor.execute(sql)
            row = cursor.fetchone()
            request_flag = item.get('request_flag')
            err_count = row[0] if row[0] else 0
            note = json.loads(row[1])  if row[1] else {}
            err_count += 1
            query_disably = 0
            if err_count > 10 :
                log.error('查询错误次数超过10次：' + str(Express_No))
                query_disably=1

            if item['err_info'] in note:
                note[item['err_info'] ] = note[item['err_info'] ] + 1
            else:
                note[item['err_info'] ] = 1

            note_content = json.dumps(note, ensure_ascii=False)

            sql = """UPDATE express SET err_count='{err_count}',request_flag='{request_flag}',query_disably='{query_disably}',note='{note}' 
                    WHERE Express_No='{Express_No}'
                 """.format(err_count=err_count,request_flag=request_flag,note=note_content,query_disably=query_disably,Express_No=Express_No)
            try:
                cursor.execute(sql)
                self.conn.commit()
            except:
                log.error('执行save_result错误,代号[002],传入item：' + str(item) + '[SQL]:'+sql)
            finally:
                pass   




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
                            phase = ','.join(t[1])
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
                SELECT i.Express_No,e.Express_Company,e.Express_Status,e.Has_Signed,i.Trace_Context,i.Trace_Date_Time,i.Trace_phase FROM express_info i
                left  JOIN  express e ON i.Express_No=e.Express_No
                WHERE i.Synchronous=1
                UPDATE express_info SET Synchronous=0
                """
        cursor.execute(sql)
        rows = cursor.fetchall()
        result = [str((i[0], i[1], i[2], i[3], i[4], i[5].strftime('%Y-%m-%d %H:%M:%S'), '0',i[6])) for i in rows]
        # print(result)
        result = ','.join([str(i) for i in result])

        self.conn.commit()
        self.conn.close()
        return result



    def repeat(self):
        """把不是签收与退回状态的快递重新放回查询池"""
        cursor = self.conn.cursor()
        sql = "UPDATE express_temp SET Process_Status=0 WHERE Express_No in (SELECT top 1000 Express_No FROM express WHERE Express_Status<>'3' AND Express_Status<>'6' AND query_disably<>'1' ORDER BY newid())"
        cursor.execute(sql)
        self.conn.commit()
        self.conn.close()


if __name__ == '__main__':
    db = Express_by_MS()
    db.save_result()
    # item = {'request_flag':'no','Express_No':'816910663902','err_info':'参数错误'}
    # n = json.dumps(item, ensure_ascii=False)
    # print(n)
    #
    #
    # #
    def push():
        db = Express_by_MS()
        item = db.save_result()

        print(item)
        if item:
            tiantu = Express_by_Tiantu()
            tiantu.push_update(item)
            print(datetime.datetime.now(), '推送单号信息')
        else:
            print("暂无需要推送的数据")

    # push()
    pass


