# -*- coding: utf-8 -*-

import config

import re, os, time, sys
import argparse
import requests
import urllib2
from pprint import pprint
import csv

import goodCoupons 
import JdItemsPage
import goodsItemsSpiderWhole
import AnalyticalURL

reload(sys)
sys.setdefaultencoding('utf-8')

# get function name
FuncName = lambda n=0: sys._getframe(n + 1).f_code.co_name
# 改变目录
os.chdir(sys.path[0])

JdCouponsSpider = goodCoupons.goodCoupons()
JdCouponsSpider.set_force(True)
JdCouponsSpider.uploaddata.set_upload_host(config.BASE_UPLOAD_COUPONS_UPDATE_HOST)


# 获取需要采集的商品ID
def get_conupons():
	r = requests.get(config.BASE_GET_COUPONS_UPDATE_HOST)
	# print r
	conupons = r.json()
	print len(conupons['data']['couponList'])
	time.sleep(100)
	if conupons['data']['couponList']:
		return conupons['data']['couponList']
	return []


def get_info(skuid, conupon_url):
	# 采集卷信息
	couponInfo = JdCouponsSpider.coupons_page(skuid, conupon_url)
	# print couponInfo
	if couponInfo['status'] == 0 and couponInfo['err'] == False:
		tmp = []
		item = {
			'skuId': couponInfo['skuid'],
			'status': '0'
		}
		tmp.append(item)
		print u'商品 ' + str(tmp[0]['skuId']) + u' | 劵状态 ' + tmp[0]['status'] + u' | 劵 ' + couponInfo['url']
		JdCouponsSpider.uploaddata.upload_json(tmp)
	return

def run():


	# 必要的登录
	print JdCouponsSpider.jd_login()

	print u'更新劵--------'
	conupons = get_conupons()

	# 劵排重
	# TODO

	i = 0
	print u'劵数量: ' + str(len(conupons))
	for conupon in conupons:
		i = i + 1
		print i
		if conupon['url'] != 'http://coupon.m.jd.com/coupons/show.action?key=9b1fe593e9f14c57a8bd158086c2ac82&roleId=6702174&to=m.jd.com':
			get_info(conupon['skuId'], conupon['url'])
			time.sleep(0.3)

def main():
	run()

main()

