# -*- coding: utf-8 -*-

# 采集京推推的劵和商品数据

import json, os, time, sys, re
import requests
import bs4
from lxml import etree

# 改变目录
os.chdir(sys.path[0])

def run():
	# 获取商品站内ID
	jingtuitui_ids = []
	ify = True
	i = 0
	while (ify):
		try:
			# 获取需要采集的商品ID
			i = i + 1
			print u'page '+ str(i)
			resp = requests.get(
				'http://www.jingtuitui.com/Index/alllist/p/' + str(i) + '.html',
				timeout = (10, 15)
			)
			print resp
			soup = bs4.BeautifulSoup(resp.text, "lxml")
			quan_goods = soup.find_all(class_='item')
			if len(quan_goods) > 0:
				ify = True
			else:
				ify = False
			for quan_good in quan_goods:
				tmp = re.findall(r"(\d+)", quan_good.find('a').get('href'))[0]
				# print tmp
				if tmp > 0:
					jingtuitui_ids.append(tmp)
		except Exception, e:
			print u'err %s', e
		time.sleep(0.3)
	print jingtuitui_ids

	fo = open("csv/json_spider_04.csv", "wb")

	# 采集商品和劵
	for jingtuitui_id in jingtuitui_ids:
		try:
			resp = requests.get(
				'http://www.jingtuitui.com/Index/detail?id=' + str(jingtuitui_id),
				timeout = (2, 3)
				)
			html = etree.HTML(resp.text)
			quan_url = html.xpath('//*[@id="mainer"]/div[1]/div/div[2]/div[5]/p[1]/a')[0].text
			item_url = html.xpath('//*[@id="mainer"]/div[1]/div/div[2]/div[5]/p[2]/a')[0].text
			print item_url, quan_url
			tmp = item_url + u',' + quan_url
			fo.write( tmp + u"\n");
		except Exception, e:
			print u'err %s', e
		time.sleep(0.1)

	fo.close()


def main():
	run()

main()






