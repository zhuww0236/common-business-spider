# -*- coding: utf-8 -*-

# 采集小豚鼠的JSON接口

import json, os, time, sys, re
# import AnalyticalURL
import requests
# from lxml import etree

# 改变目录
os.chdir(sys.path[0])


# analyticalurl = AnalyticalURL.AnalyticalURL()

def get_url_from_content(content):
	pattern = re.compile(r'((?:http|https)://[\w\-\.,@?^=%&:\/~\+#]+)')
	return re.findall(pattern, content)

def run():
	fo = open("csv/json_spider_02.csv", "wb")

	ify = True
	i = 0
	while (ify):
		# 获取需要采集的商品ID
		i = i + 1
		r = requests.get(
			'http://www.xiaotunshu.net/findJdPopProds.jhtml?authorid=4&token=2DC071D4AE444EEDAE7C68&stepSize=50&page=' + str(i),
			timeout = (4, 6)
		)
		print r
		items = r.json()
		if len(items['list']) > 0:
			ify = True
		else:
			ify = False

		for item in items['list']:
			if not item.has_key('couponlink'):
				continue
			if len(get_url_from_content(item['couponlink'])) != 1:
				continue
			tmp_con = item['couponlink']
			# print str(item['skuid']), tmp_con
			tmp = u'http://item.jd.com/' + str(item['skuid']) + u'.html,' + tmp_con
			try:
				fo.write( tmp + u"\n");
			except Exception, e:
				print u'err %s', e
		time.sleep(0.1)
	fo.close()

def main():
	run()

main()
