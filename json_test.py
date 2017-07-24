# -*- coding: utf-8 -*-

# json文件读取

import json, os, time, sys, re
import JdItemsPage
import requests
from lxml import etree

JdItemsPage = JdItemsPage.JdItemsPage()

def revertShortLink(url):
    res = requests.head(url)
    return res.headers.get('location')

with open('json_data01.txt', 'r') as f:
    data = json.load(f)

sess = requests.Session()
for item in data['data']:
	print item['quanLink']
	continue
	lurl = revertShortLink(item['quanLink']).replace(' ', '')

	# 解析出 key 和 roleId 的值
	# key
	try:
		key = re.findall(r"\?key\=(\w{32})\&", lurl)
		if len(key) < 1:
			key = re.findall(r"\?keyid\=(\w{32})\&", lurl)
		if len(key) < 1:
			key = re.findall(r"\%3Fkey\%3D(\w{32})\%26", lurl)
		if len(key) < 1:
			continue
	except Exception, e:
		print item['quanLink'], lurl
		continue


	# roleId
	try:
		roleId = re.findall(r"\&roleId\=(\d+)\&", lurl)
		if len(roleId) < 1:
			roleId = re.findall(r"\&roleid\=(\d+)\&", lurl)
		if len(roleId) < 1:
			roleId = re.findall(r"\%26roleId\%3D(\d+)\%26", lurl)
		if len(roleId) < 1:
			continue
	except Exception, e:
		# print item['quanLink'], lurl
		continue
	# print key, roleId
	couponsurl = u'http://coupon.m.jd.com/coupons/show.action?key=' + str(key[0]) + '&roleId=' + str(roleId[0]) + '&to=mall.jd.com/'
	# print couponsurl
	# print u'------------------------------'
	itemUrl = 'https://item.jd.com/' + str(item['taobaoItemId']) + '.html'

	# JdItemsPage.set_sess(self.sess)
	# JdItemsPage.set_cookies(self.cookies)
	jditem = JdItemsPage.items_page_from_xpath(itemUrl)
	print jditem

	# try:
	# 	resp = sess.get(
	# 		itemUrl
	# 	)
	# except Exception, e:
	# 	print u'get goods page err :'
	# html = etree.HTML(resp.text)
	# try:
	# 	result = html.xpath('//*[@id="crumb-wrap"]/div/div[1]/div[1]/a')
	# 	if len(result) < 1:
	# 		result = html.xpath('//*[@id="root-nav"]/div/div/strong/a')
	# 	category1name = result[0].text
	# except Exception, e:
	# 	print u'get category1 err'
	# 	print itemUrl
	# 	category1name = ''
	# # print category1name
	print itemUrl + ',' + jditem['category1name'] + ',' + couponsurl + ',,,,,,'
	time.sleep(1)





