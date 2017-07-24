# -*- coding: utf-8 -*-
# 
# 京东商品详情页
# 

import config

import bs4
import requests, requests.packages.urllib3
import re, os, time, sys
import logging, logging.handlers
import urlparse
import json
import SqliteData


requests.packages.urllib3.disable_warnings()
reload(sys)
sys.setdefaultencoding('utf-8')

class JdItemsPage():

	def __init__(self):
		# logger = logging.getLogger('JdItemsPageLogger')
		# logger.setLevel(logging.INFO)
		# rh=logging.handlers.TimedRotatingFileHandler('log/jditemspagelogger.log','D')
		# fm=logging.Formatter("%(asctime)s  %(levelname)s - %(message)s","%Y-%m-%d %H:%M:%S")
		# rh.setFormatter(fm)
		# logger.addHandler(rh)
		# self.infolog=logger.info
		# self.errorlog=logger.error

		self.sess = requests.Session()
		self.cookies = {}
		self.headers = {
			'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
			'ContentType': 'text/html; charset=utf-8',
			'Accept-Encoding':'gzip, deflate, sdch',
        	'Accept-Language':'zh-CN,zh;q=0.8',
			'Connection' : 'keep-alive',
		}
		self.proxies = {
			"http": "http://115.210.201.179:8998", 
			"http": "http://221.232.194.130:808",
			"http": "http://117.90.5.76:9000",
		}

		self.err_sleep_time = config.SLEEP_TIMEPAGE_ERR
		self.timeout_doogs_page_connect = config.TIMEOUT_DOOGS_PAGE_CONNECT
		self.timeout_doogs_page_request = config.TIMEOUT_DOOGS_PAGE_REQUEST

		self.sqlitedata = SqliteData.SqliteData()
		self.force = False



	def set_sess(self, sess):
		self.sess = sess

	def set_cookies(self, cookies):
		self.cookies = cookies



	def set_force(self, switch = False):
		self.force = switch



	# 从库读取劵信息
	def read_items_4_table(self, skuid):
		if skuid < 1:
			return {}
		tmp = self.sqlitedata.read_items(skuid)
		if tmp == False or len(tmp) < 1:
			return {}

		# 设置过期时间
		a = datetime.datetime.now()
		b = a - datetime.timedelta(hours=2)
		# 获取最后更新时间
		c = datetime.datetime.strptime(tmp[2], "%Y-%m-%d %H:%M:%S")
		# 如果低于最后更新时间，则返回空
		if c < b:
			return {}
		else:
			return tmp[4]



	# 写劵信息到库
	def write_items_4_table(self, skuid, item_info):
		return self.sqlitedata.write_items(skuid, item_info)



	def get_category1_id(self, category1_name):
		if category1_name == '数码产品':
			return '173'
		elif category1_name == '电脑产品':
			return '174'
		elif category1_name == '电脑附件':
			return '175'
		elif category1_name == '数码':
			return '652'
		elif category1_name == '电脑、办公':
			return '670'
		elif category1_name == '电脑办公':
			return '670'
		elif category1_name == '家用电器':
			return '737'
		elif category1_name == '日用百货':
			return '911'
		elif category1_name == '服饰内衣':
			return '1315'
		elif category1_name == '美妆个护':
			return '1316'
		elif category1_name == '运动户外':
			return '1318'
		elif category1_name == '母婴':
			return '1319'
		elif category1_name == '食品饮料':
			return '1320'
		elif category1_name == '家居家装':
			return '1620'
		elif category1_name == '礼品箱包':
			return '1672'
		elif category1_name == '图书':
			return '1713'
		elif category1_name == '音乐':
			return '4051'
		elif category1_name == '影视':
			return '4052'
		elif category1_name == '教育音像':
			return '4053'
		elif category1_name == '本地生活/旅游出行':
			return '4938'
		elif category1_name == '钟表':
			return '5025'
		elif category1_name == '电子书':
			return '5272'
		elif category1_name == '网络原创':
			return '5273'
		elif category1_name == '珠宝首饰':
			return '6144'
		elif category1_name == '厨具':
			return '6196'
		elif category1_name == '玩具乐器':
			return '6233'
		elif category1_name == '汽车用品':
			return '6728'
		elif category1_name == '宠物生活':
			return '6994'
		elif category1_name == '医药保健':
			return '9192'
		elif category1_name == '医疗保健':
			return '9192'
		elif category1_name == '卖家服务':
			return '9669'
		elif category1_name == '家具':
			return '9847'
		elif category1_name == '家装建材':
			return '9855'
		elif category1_name == '手机':
			return '9987'
		elif category1_name == '鞋靴':
			return '11729'
		elif category1_name == '生鲜':
			return '12218'
		elif category1_name == '酒类':
			return '12259'
		elif category1_name == '京东通信':
			return '12362'
		elif category1_name == '农用物资':
			return '12473'
		else:
			return False


	# 使用 xpath 获取分类信息
	def items_page_from_xpath(self, url):
		return self.items_page_m(url)



	def items_page(self, url):
		return self.items_page_m(url)



	def items_page_pc(self, url):
		return self.items_page_pc_new(url)



	def items_page_pc_new(self, url):
		rs = urlparse.urlparse(url)
		try:
			resp = self.sess.get(
				url,
				cookies = self.cookies,
				headers = self.headers,
				timeout = (self.timeout_doogs_page_connect, self.timeout_doogs_page_request)
			)
		except Exception, e:
			# self.errorlog('get items page err : %s', e)
			return False

		try:
			# good page
			soup = bs4.BeautifulSoup(resp.text, "lxml")
		except Exception, e:
			# self.errorlog('get items page err : %s', e)
			return False

		# 获取商品JS信息
		try:
			tmp = soup.select('html > head > script')
			js_str = tmp[0].get_text()
		except Exception, e:
			return False

		# 分类ID列表
		category1 = ''
		categorys = []
		try:
			category_id_tmp = re.findall(r'cat: \[(\S+)\]', js_str)[0].split(',')
			for category_id in category_id_tmp:
				tmp = category_id.strip().strip('"')
				categorys.append(tmp)
			category1 = categorys[0]
		except Exception, e:
			return False

		# 商品图片
		images = []
		try:
			img_list_tmp = re.findall(r'imageList: \[(\S+)\]', js_str)[0].split(',')
			for img in img_list_tmp:
				tmp = u'https://m.360buyimg.com/n12/' + img.strip().strip('"') + u'!q70.jpg'
				images.append(tmp)
		except Exception, e:
			images = []

		# 获取商品ID
		try:
			skuid = re.findall(r'skuid: ?(\d+),?', js_str)[0]
		except Exception, e:
			skuid = ''
		
		# 获取商品自营信息
		try:
			tmp = re.findall(r'isPop: ?(false) ?,', js_str)[0]
			if tmp == 'false':
				adownerType = 'g'
			else:
				adownerType = 'p'
		except Exception, e:
			adownerType = 'p'
		
		# 获取商品关联ID
		link_skuid = []
		try:
			skuid_list_tmp = re.findall(r'colorSize: \[(\S+)\]', js_str)[0]
			link_skuid = re.findall(r'"skuId":(\d+),', skuid_list_tmp)
		except Exception, e:
			link_skuid = []

		'''
		# 获取商品发货信息
		# text = soup.find('div', class_='summary-service').find('span', class_='hl_red')
		text = soup.find('div', id='summary-service')
		print text.find_all('a', class_='hl_red') 
		print soup.select('#summary-service')
		if text == u'京东':
			fh = '1'
		else:
			fh = '0'
		'''

		item = {
			'id': skuid,
			'adownerType': adownerType,
			'category1': category1,
			'images': images,
			# 'selfDispatch': '',
			'linkSkuid': link_skuid,
		}
		return item



	# 移动版商品价格
	def items_page_m_get_price(self, skuid):
		return self.get_item_price_4_3cn(skuid)
		
		url = 'https://item.m.jd.com/product/' + str(skuid) + '.html'
		try:
			resp = self.sess.get(
				url,
				cookies = self.cookies,
				headers = self.headers,
				# proxies = self.proxies,
				timeout = (self.timeout_doogs_page_connect, self.timeout_doogs_page_request)
			)
		except Exception, e:
			# self.errorlog('get items page err : %s', e)
			return {}

		try:
			# m good page
			soup = bs4.BeautifulSoup(resp.text, "lxml")

			# 获取商品关联 skuid 列表
			price = ''
			text = soup.find(id='jdPrice')['value']
			if len(text) > 0:
				price = text
			return price
		except Exception, e:
			# print e
			return ''



	# 接口获取商品价格
	def get_item_price_4_3cn(self, skuid):
		url = 'http://pm.3.cn/prices/pcpmgets?callback=jQuery&skuids=' + str(skuid) + '&origin=2'
		try:
			resp = self.sess.get(
				url,
				cookies = self.cookies,
				headers = self.headers,
				timeout = (self.timeout_doogs_page_connect, self.timeout_doogs_page_request)
			)
		except Exception, e:
			return ''

		try:
			item = json.loads(resp.text.replace('jQuery(', '').replace(');', ''))
			if len(item[0]['p']) < 1:
				return ''
			else:
				return item[0]['p']
		except Exception, e:
			return ''



	# 移动版商品详情
	def items_page_m(self, url):
		rs = urlparse.urlparse(url)
		try:
			resp = self.sess.get(
				url,
				cookies = self.cookies,
				headers = self.headers,
				# proxies = self.proxies,
				timeout = (self.timeout_doogs_page_connect, self.timeout_doogs_page_request)
			)
		except Exception, e:
			# self.errorlog('get items page err : %s', e)
			return {}

		try:
			# m good page
			soup = bs4.BeautifulSoup(resp.text, "lxml")

			# 获取商品图片列表
			text = soup.select('#slide > ul > li')
			ify = False
			images = []
			for div in text:
				tmp = div.find('img').get('imgsrc')
				if tmp != None:
					images.append(tmp)

			# 获取商品ID
			text = soup.find(id='currentWareId')['value']
			if len(text) < 1:
				return False
			skuid = text

			# 获取商品分类
			text = soup.find(id='categoryId')['value']
			# print text
			category1 = text.split('_')[0]
			# print category1
			if text == category1 or len(text) < 1:
				category1 = ''
		
			# 获取商品自营信息
			text = soup.select('#mainLayout > div.goods-part.bdr-tb.price-floor > div > div.prod-title > a > span > i')
			if len(text) > 0:
				# 自营
				adownerType = 'g'
			else:
				adownerType = 'p'

			# 获取商品发货信息
			text = soup.select('#mainLayout > div.service-floor.J_ping > div.service-tip-module')
			ify = False
			for div in text:
				tmp = div.find('span', class_='service-icon-text').getText()
				if tmp == u'京东发货&售后' or tmp == u'京东发货&店铺售后':
					ify = True
			if ify:
				# 京东发货
				fh = '1'
			else:
				fh = '0'

			# 获取商品关联 skuid 列表
			link_skuid = []
			text = soup.find(id='skuColorSizeSpec')['value']
			if len(text) > 0:
				tmp = json.loads(text)
				for l_skuid in tmp['colorSize']:
					link_skuid.append(l_skuid['skuId'])
			
			item = {
				'id': skuid,
				'adownerType': adownerType,
				'category1': category1,
				'images': images,
				'linkSkuid': link_skuid,
				'selfDispatch': fh
			}
			return item
		except Exception, e:
			# print e
			return {}



