# -*- coding: utf-8 -*-

# 采集友邻的JSON接口

import json, os, time, sys, re, platform
import requests
from lxml import etree

# 改变目录
os.chdir(sys.path[0])

def run():
	# from selenium import webdriver
	# from selenium.webdriver.common.by import By
	# from selenium.webdriver.support.ui import WebDriverWait
	# from selenium.webdriver.support import expected_conditions as EC

	sess = requests.Session()
	headers = {
		'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
		'ContentType': 'text/html; charset=utf-8',
		'Accept-Encoding':'gzip, deflate, sdch',
		'Accept-Language':'zh-CN,zh;q=0.8',
		'Connection' : 'keep-alive',
		'Referer' : 'http://www.lanyincao.com/console/',
	}
	cookies = {}


	'''
	def get_url_from_content(content):
		pattern = re.compile(r'((?:http|https)://[\w\-\.,@?^=%&:\/~\+#]+)')
		return re.findall(pattern, content)

	def get_cookies():
		osName = platform.system()
		if osName == 'Windows':
			driver = webdriver.Chrome('./chromedriver.exe')
		else:
			driver = webdriver.Chrome('./chromedriver')
		# 京东移动页面登录
		driver.get('http://www.lanyincao.com/console/')
		time.sleep(5)
		driver.find_element_by_id("username").send_keys('redrum0003')
		time.sleep(1)
		driver.find_element_by_id("password").send_keys('redrum0003')

		# 等待登录完成页
		element = WebDriverWait(driver, 1200).until(
			EC.presence_of_element_located((By.CLASS_NAME, "entypo-user"))
		)

		# 从 driver 获取 cookies 
		cookie_list = driver.get_cookies()
		# 读取有用的 cookies 信息
		cookie_dict = {}
		for cookie in cookie_list:
			if cookie.has_key('name') and cookie.has_key('value'):
				cookie_dict[cookie['name']] = cookie['value']
		cookies = cookie_dict

		time.sleep(5)
		# 关闭 driver
		driver.quit()
		return cookies

	yl_cookies = get_cookies()
	fo = open("csv/json_spider_yl.csv", "wb")

	ify = True
	i = 0
	while (ify):
		i = i + 1
		# 获取需要采集的商品ID
		resp = sess.get(
			'http://www.lanyincao.com/console/console/item/getlist?page=' + str(i)  + '&shops=3&commissionType=3&sort=addtime&sortType=desc&catId=0&search=', 
			headers = headers,
			cookies = yl_cookies
			)
		print resp
		items = resp.json()
		if not items.has_key('data'):
			ify = False
			continue

		if len(items['data']) > 0:
			ify = True
		else:
			ify = False
			continue

		for item in items['data']:
			if not item.has_key('quanLink'):
				continue
			if len(get_url_from_content(item['quanLink'])) != 1:
				continue
			tmp_con = item['quanLink']
			try:
				# print str(item['taobaoItemId']), tmp_con
				tmp = 'http://item.jd.com/' + str(item['taobaoItemId']) + '.html,' + tmp_con
				fo.write( tmp + "\n");
			except Exception, e:
				print (' err : %s', e)
		time.sleep(1)

	ify = True
	while (ify):
		i = i + 1
		# 获取需要采集的商品ID
		resp = sess.get(
			'http://www.lanyincao.com/console/console/item/getlist?page=' + str(i)  + '&shops=3&commissionType=9&sort=addtime&sortType=desc&catId=0&search=&beginPrice=&endPrice=&beginYj=&endYj=&upYjRate=', 
			headers = headers,
			cookies = yl_cookies
			)
		print resp
		items = resp.json()
		if not items.has_key('data'):
			ify = False
			continue

		if len(items['data']) > 0:
			ify = True
		else:
			ify = False
			continue

		for item in items['data']:
			if not item.has_key('quanLink'):
				continue
			if len(get_url_from_content(item['quanLink'])) != 1:
				continue
			tmp_con = item['quanLink']
			try:
				# print str(item['taobaoItemId']), tmp_con
				tmp = 'http://item.jd.com/' + str(item['taobaoItemId']) + '.html,' + tmp_con
				fo.write( tmp + "\n");
			except Exception, e:
				print (' err : %s', e)
		time.sleep(1)

	fo.close()
	'''

	fo = open("csv/json_spider_yl.csv", "wb")

	ify = True
	i = 0
	'''
	app-secret	string	是	签名
	app-key		string	是	账号
	unionId		long	是	联盟ID
	pid			long	是	推广位ID
	page		int		是	当前页数
	pageSize	int		否	最大为100
	type		int		否	优惠形式
							0为所有，5为优惠券
	activity	int		否	活动类别	
							0为所有，9为爆款
	'''
	yl_activity = '0'
	yl_type = '5'
	while (ify):
		i = i + 1
		# 获取需要采集的商品ID
		url = 'http://www.lanyincao.com/console/openapi/items?unionId=1000144672&pid=712114882&pageSize=100&app-key=tkcat&app-secret=adaec03f-6148-44cf-b13a-8d4d45aa9a24&sku=&activity=' + str(yl_activity) + '&type=' + str(yl_type) + '&page=' + str(i)
		resp = sess.post(
			url,
			headers = headers,
			timeout = (2, 3)
		)
		print resp
		try:
			items = resp.json()
		except Exception, e:
			print (' 解析 json 出错 : %s', e)
			print url
			continue

		if not items.has_key('list'):
			ify = False
			continue

		if len(items['list']) > 0:
			ify = True
		else:
			ify = False
			continue

		for item in items['list']:
			if not item.has_key('quanUrl'):
				continue
			tmp_con = item['quanUrl']
			try:
				tmp = 'http://item.jd.com/' + str(item['sku']) + '.html,' + tmp_con
				fo.write( tmp + "\n");
			except Exception, e:
				print (' err : %s', e)
		time.sleep(0.5)

	fo.close()


def main():
	run()

main()

