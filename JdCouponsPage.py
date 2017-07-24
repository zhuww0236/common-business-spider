# -*- coding: utf-8 -*-

# 京东密卷页面解析规则

import config

import bs4
import requests, requests.packages.urllib3
import re, os, time, sys
import logging, logging.handlers
import urlparse
import sqlite3
import SqliteData
import datetime

requests.packages.urllib3.disable_warnings()
reload(sys)
sys.setdefaultencoding('utf-8')

class JdCouponsPage():

	def __init__(self):
		logger = logging.getLogger('JdCouponsPageLogger')
		logger.setLevel(logging.INFO)
		rh=logging.FileHandler('log/jdcouponspage.log')
		fm=logging.Formatter("%(asctime)s  %(levelname)s - %(message)s","%Y-%m-%d %H:%M:%S")
		rh.setFormatter(fm)
		logger.addHandler(rh)
		self.infolog=logger.info
		self.errorlog=logger.error

		self.sess = object
		self.cookies = {}
		self.headers = {
			'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
			'ContentType': 'text/html; charset=utf-8',
			'Accept-Encoding':'gzip, deflate, sdch',
        	'Accept-Language':'zh-CN,zh;q=0.8',
			'Connection' : 'keep-alive',
		}
		self.err_sleep_time = config.SLEEP_TIMEPAGE_ERR
		self.timeout_doogs_page_connect = config.TIMEOUT_DOOGS_PAGE_CONNECT
		self.timeout_doogs_page_request = config.TIMEOUT_DOOGS_PAGE_REQUEST

		self.cookie_file = config.BASE_MJD_COOKIE_FILE

		self.sqlitedata = SqliteData.SqliteData()
		self.force = False



	def set_sess(self, sess):
		self.sess = sess



	def set_cookies(self, cookies):
		self.cookies = cookies



	def set_force(self, switch = False):
		self.force = switch



	# 从文件中反序列化到 cookies
	def load_cookies_to_file(self):
		try:
			with open(self.cookie_file, 'rb') as f:
				self.cookies = pickle.load(f)
		except Exception as e:
			self.errorlog("mjd cookies load to file False %s", e)
			print (u"mjd cookies load to file False %s", e)
		return



	# 更新 cookies 然后再次请求
	def re_resp(self, url):
		self.load_cookies_to_file()
		try:
			resp = self.sess.get(
				url,
				cookies = self.cookies,
				headers = self.headers,
				timeout = (self.timeout_doogs_page_connect, self.timeout_doogs_page_request)
			)
			return resp.text
		except Exception, e:
			self.errorlog('re get coupons page err : %s', e)
			print u're get coupons page err : %s', e
			return None



	# 从库读取劵信息
	def read_coupons_4_table(self, skuid, url):
		tmp = self.sqlitedata.read_coupons(url)
		if tmp == False or len(tmp) < 1:
			return {}
		tmp = tmp[0]
		# 设置过期时间
		a = datetime.datetime.now()
		b = a - datetime.timedelta(hours=2)
		# 获取最后更新时间
		c = datetime.datetime.strptime(tmp[10], "%Y-%m-%d %H:%M:%S")
		# 如果低于最后更新时间，则返回空
		if c < b:
			return {}
		else:
			return {
				'status': tmp[3],
				'skuid': skuid,
				'err': False,
				'url': tmp[6],
				'value': tmp[4],
				'restrict': tmp[5],
				'startTime': tmp[7],
				'endTime': tmp[8],
			}



	# 写劵信息到库
	def write_coupons_4_table(self, coupon_info):
		return self.sqlitedata.write_coupons(coupon_info)


	# 从网络获取劵信息
	def coupons_page(self, skuid, url):
		container = {
			'status': 0,
			'skuid': skuid,
			'err': True,
			'url': url
		}

		if self.force == False:
			# 先从库中读取，节省网络资源
			tmp = self.read_coupons_4_table(skuid, url)
			if len(tmp) > 0:
				print u'库中存在劵，获取...'
				return tmp

		try:
			resp = self.sess.get(
				url,
				cookies = self.cookies,
				headers = self.headers,
				timeout = (self.timeout_doogs_page_connect, self.timeout_doogs_page_request)
			)
			resp_text = resp.text
			# print resp.text
		except Exception, e:
			self.errorlog('get coupons page err : %s', e)
			print u'get coupons page err : %s', e
			tmp = self.re_resp(url)
			if tmp == None:
				return container
			else:
				resp_text = tmp


		try:
			# coupons page
			soup = bs4.BeautifulSoup(resp_text, "lxml")
			# 检查该 URL 是否有效
			coupon_fail_result = soup.find("div", class_="coupon-content-container fail_result")
			# print u'检查该 URL 是否有效'
			if coupon_fail_result != None:
				# print u'URL 地址无效'
				return container
			# print u'有效'

			# 检查该劵是否可以领取
			coupon_active = soup.find("a", id="btnSubmit").getText()
			# print u'检查该劵是否可以领取'
			if coupon_active != '立即领取':
				container['err'] = False
				return container

			containerSoup = soup.find('div', class_='coupon-box coupon-dong')

			# 获取劵价格
			money = containerSoup.find('p', class_="money").find('strong').getText()

			# 获取劵规则
			tmp = containerSoup.find('p', class_="rule").getText()
			if tmp == None:
				container['err'] = False
				return container
			rule = re.findall(r"(\d+)", tmp)[0]

			# 获取时间
			tmp = containerSoup.find('p', class_="use-time").getText()
			if tmp == None:
				container['err'] = False
				return container

			use_times = re.findall(r"(\d{4}\.\d{2}\.\d{2}\ \d{2}\:\d{2})", tmp)
			use_time_start = use_times[0].replace('.', '-') + ':00'
			use_time_end = use_times[1].replace('.', '-') + ':59'

			container = {
				'status': 1,
				'skuid': skuid,
				'err': False,
				'url': url,
				'value': money,
				'restrict': rule,
				'startTime': use_time_start,
				'endTime': use_time_end
			}
			self.write_coupons_4_table(container)
		except Exception, e:
			print u'Soup err %s', e
			self.errorlog('Soup err %s', e)
		return container
