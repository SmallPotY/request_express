# coding=utf-8

import model
from apscheduler.schedulers.blocking import BlockingScheduler
import datetime

# db = model.Express_by_MS()

# db.get_temp_express()

# print(datetime.datetime.now(), "更新快递查询池")


def update(q):
    db = model.Express_by_MS()
    db.get_temp_express(q)
    print(datetime.datetime.now(), "更新快递查询池")


def push():
    db = model.Express_by_MS()
    item = db.get_push()

    tiantu = model.Express_by_Tiantu()
    tiantu.push_update(item)
    print(datetime.datetime.now(),'推送单号信息')



#
# scheduler = BlockingScheduler()
# scheduler.add_job(func=update, trigger='interval', seconds=60)
# scheduler.add_job(func=push, trigger='interval', seconds=60)
# scheduler.start()
