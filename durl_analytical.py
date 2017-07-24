# -*- coding: utf-8 -*-

# 短链接测试

import json, os, time, sys, re
import JdItemsPage
import requests
import AnalyticalURL
from lxml import etree

analyticalurl = AnalyticalURL.AnalyticalURL()

import JdCompoundSpiderClass

jdcompoundspiderclass = JdCompoundSpiderClass.JdCompoundSpiderClass()

def revertShortLink(url):
    res = requests.head(url)
    return res.headers.get('location')


# 删除商品链接结尾的特殊字符
def filter_item_url(url):
	# 删除结尾 - 字符
	tmp = url.strip().lstrip().rstrip(',').rstrip('-')
	# 删除结尾 SKU:xxxx
	tmp2 = re.findall(r'((?i)SKU: ?\d+)$', tmp)
	if len(tmp2) > 0:
		tmp = tmp.replace(tmp2[0], '')
	# 删除结尾 SKUID:xxxx
	tmp2 = re.findall(r'((?i)SKU： ?\d+)$', tmp)
	if len(tmp2) > 0:
		tmp = tmp.replace(tmp2[0], '')
	return tmp


def check_url_type(urls):
	url_type = None
	if len(urls) != 2:
		return url_type

	if len(re.findall(r'[http|https]\:\/\/item\.jd\.com\/(\d+).html', urls[1])) > 0:
		url_type = {
			'conupon_url' : urls[0],
			'item_url' : filter_item_url(urls[1])
		}
		return url_type
	elif len(re.findall(r'[http|https]\:\/\/union\-click\.jd\.com\/(\w+)', urls[1])) > 0:
		url_type = {
			'conupon_url' : urls[0],
			'item_url' : filter_item_url(urls[1])
		}
		return url_type
	elif len(re.findall(r'[http|https]\:\/\/item\.m\.jd\.com\/ware\/view\.action\?wareId\=(\d+)', urls[1])) > 0:
		url_type = {
			'conupon_url' : urls[0],
			'item_url' : filter_item_url(urls[1])
		}
		return url_type
	else:
		# 循环解析302跳转
		# tmp = jdcompoundspiderclass.analyticalurl.analytica_for_durl(urls[0])
		# if tmp != None:
		# 	# 如果解析发现是302跳转，使用解析后的内容
		# 	urls[0] = tmp
		tmp = jdcompoundspiderclass.analyticalurl.analytica_for_durl(urls[1])
		print u'urls setp 1'
		print tmp
		if tmp != None and tmp != 'https://www.jd.com/?d':
			# 如果解析发现是302跳转，使用解析后的内容
			urls[1] = tmp
		print u'urls setp 2'
		print urls
		if jdcompoundspiderclass.analyticalurl.analytica_durl(urls[0]) == 'is coupon' and jdcompoundspiderclass.analyticalurl.analytica_durl(urls[1]) == None:
			url_type = {
				'conupon_url' : urls[0],
				'item_url' : filter_item_url(urls[1])
			}
			return url_type
	# print url_type
	return url_type


url = 'http://t.cn/RaWQ30X'
url = 'https://union-click.jd.com/jdc?d=IDlZ3W&come=appmessage'
url = 'http://dwz.cn/5YiuvZ'
url = 'https://union-click.jd.com/jdc?d=uhETOM'

# print revertShortLink(url)
# print "======================="
# r = requests.Session().get(
#     url
# )
# print r.text
# hrl = re.findall(r"\; hrl=\'(.+)\' \;", r.text)
# print hrl
# print revertShortLink(hrl[0])


# print analyticalurl.analytica_for_durl(url)
print analyticalurl.get_real_coupon_url(url)
print analyticalurl.get_real_item_url(url)


ss = 'https://union-click.jd.com/jdc?d=uhETOMSKU:10650650935'
tmp = re.findall(r'[http|https]\:\/\/union\-click\.jd\.com\/(\w+)', ss)
print ss, tmp
print check_url_type(['http://dwz.cn/5XpmRy', 'https://union-click.jd.com/jdc?d=uhETOMSKU:10650650935'])