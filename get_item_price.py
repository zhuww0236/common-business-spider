# -*- coding: utf-8 -*-

# 短链接测试

import json, os, time, sys, re
import JdItemsPage
import requests
import ExistingCommodity
import MjdLogin

jditemspage = JdItemsPage.JdItemsPage()
existingcommodity = ExistingCommodity.ExistingCommodity()
mjdlogin = MjdLogin.MjdLogin()

# 登录
mjdlogin.check_login()
jditemspage.set_sess(mjdlogin.get_sess())
jditemspage.set_cookies(mjdlogin.get_cookies())

fo = open("csv/goods_price.txt", "wb")

# 按照商品ID来更新价格
existingcommodity.get_data()
skuids = existingcommodity.load_skuids()
print u'总数: '+ str(len(skuids))
i = 0
for skuid in skuids:
    i = i + 1
    price = jditemspage.items_page_m_get_price(skuid)
    print i, skuid, price
    if price != '' and price != u'暂无报价':
        sql_str = str(skuid) + '=' + str(price)
        fo.write( sql_str + "\n");
    time.sleep( 0.1 )
fo.close()
