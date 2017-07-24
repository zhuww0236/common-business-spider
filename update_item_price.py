# -*- coding: utf-8 -*-

# 通过接口获取需要更新价格的商品ID并更新价格

import config

import json, os, time, sys, re
import JdItemsPage
import requests
import UploadData
import MjdLogin

# 改变目录
os.chdir(sys.path[0])

def run():
    jditemspage = JdItemsPage.JdItemsPage()
    uploaddata = UploadData.UploadData()
    mjdlogin = MjdLogin.MjdLogin()

    # 登录
    mjdlogin.check_login()
    jditemspage.set_sess(mjdlogin.get_sess())
    jditemspage.set_cookies(mjdlogin.get_cookies())

    # 设置上传地址
    uploaddata.set_upload_host(config.BASE_UPLOAD_ITEM_PRICE_UPDATE_HOST)
    uploaddata.set_csv_file_path('csv/ttt.csv')
    uploaddata.set_csv_uniq_file_path('csv/ttt.csv')

    # 获取商品ID
    r = requests.get(config.BASE_GET_ITEM_PRICE_UPDATE_HOST)
    # print r
    tmp = r.json()
    skuids = []
    if tmp['data']['skuIdList']:
    	skuids = tmp['data']['skuIdList']


    # 按照商品ID来更新价格
    print u'总数: '+ str(len(skuids))
    i = 0
    items = []
    for skuid in skuids:
        i = i + 1
        price = jditemspage.items_page_m_get_price(skuid)
        print i, skuid, price
        if price != '' and price != u'暂无报价':
            sql_str = str(skuid) + '=' + str(price)
            tmp = {
            	'skuId': str(skuid),
            	'price': str(price)
            }
            items.append(tmp)
        time.sleep( 0.1 )

    # print items

    # 上传
    uploaddata.upload_json(items)

def main():
    run()

main()