# -*- coding: utf-8 -*-

# json文件读取

import json, os, time, sys, re
import AnalyticalURL
import requests
from lxml import etree

# 改变目录
os.chdir(sys.path[0])

def run():
	analyticalurl = AnalyticalURL.AnalyticalURL()

	fo = open("csv/json_spider_01.csv", "wb")

	ify = True
	i = 0
	while (ify):
		# 获取需要采集的商品ID
		i = i + 1
		r = requests.get(
			'http://if.qiubixiong.com/g_data.php?page=' + str(i),
			timeout = (2, 3)
		)
		print r
		items = r.json()
		if len(items) > 0:
			ify = True
		else:
			ify = False

		for item in items:
			tmp_con = analyticalurl.get_real_coupon_url(item['inner_coupon'])
			if tmp_con != None:
				tmp = 'http://item.jd.com/' + item['sku'] + '.html,' + tmp_con
				fo.write( tmp + "\n");
		time.sleep(1)
	fo.close()

def main():
	run()

main()
