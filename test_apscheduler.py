# -*- coding: utf-8 -*-

import os, time
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
import logging

# logging.basicConfig()

def job_function():
    print("Fuck World")


def goodsitemsspiderwhole():
    import goodsItemsSpiderWhole
    jd = goodsItemsSpiderWhole.goodsItemsSpiderWhole()
    print u'采集开始'
    if not jd.jd_login():
        return
    jd.category_list([])
    print u'采集结束'
    print u'开始上传数据'
    jd.upload_json_whole()
    print u'上传数据结束'


def updateItemPrice():
    import update_item_price
    update_item_price.main()


def json_spider_01():
    import json_spider_01
    import JdCompoundSpider
    json_spider_01.main()
    JdCompoundSpider.main(['xclm'])


def json_spider_02():
    import json_spider_02
    import JdCompoundSpider
    json_spider_02.main()
    JdCompoundSpider.main(['xts'])


def json_spider_03():
    import json_spider_03
    import JdCompoundSpider
    json_spider_03.main()
    JdCompoundSpider.main(['yl'])


def json_spider_04():
    import json_spider_04
    import JdCompoundSpider
    json_spider_04.main()
    JdCompoundSpider.main(['jtt'])


def couponsUpdate():
    import couponsUpdate
    couponsUpdate.main()



def zs():
    # 阻塞方式
    # BlockingScheduler
    sched = BlockingScheduler()
    sched.add_job(job_function, 'interval', seconds=5)
    sched.add_job(job_function2, 'interval', seconds=2)
    print(u'Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
    # sched.add_listener(err_listener, sched.events.EVENT_JOB_ERROR | sched.events.EVENT_JOB_MISSED | EVENT_SCHEDULER_START) 
    try:
        sched.start()  #采用的是阻塞的方式，只有一個線程專職做調度的任務
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        sched.shutdown()
        print('Exit The Job!')

def fzs():
    # 非阻塞方式
    # BlockingScheduler
    sched = BackgroundScheduler()
    # sched.add_job(goodsitemsspiderwhole, 'interval', hours=8)
    sched.add_job(updateItemPrice, 'interval', seconds=120)
    # sched.add_job(json_spider_01, 'interval', hours=12)
    # sched.add_job(json_spider_02, 'interval', hours=12)
    # sched.add_job(json_spider_03, 'interval', hours=12)
    # sched.add_job(json_spider_04, 'interval', hours=12)
    sched.add_job(couponsUpdate, 'interval', hours=4)
    sched.start()
    print(u'Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
    try:
        while True:
            # sched.print_jobs()
            time.sleep(2)  #其他任務是獨立的線程執行
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        sched.shutdown()
        print('Exit The Job!')

fzs()