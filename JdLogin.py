# -*- coding: utf-8 -*-

import config

import bs4
import requests, requests.packages.urllib3
import re, os, time, sys, platform
import logging, logging.handlers
import pickle
import random
import json
import argparse
import random
import subprocess

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

requests.packages.urllib3.disable_warnings()
reload(sys)
sys.setdefaultencoding('utf-8')

class JdLogin():

	def __init__(self):
		
		self.sess = requests.Session()
		self.headers = {
			'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
			'ContentType': 'text/html; charset=utf-8',
			'Accept-Encoding':'gzip, deflate, sdch',
        	'Accept-Language':'zh-CN,zh;q=0.8',
			'Connection' : 'keep-alive',
		}
		self.cookies = {}
		self.cookie_file = config.BASE_COOKIE_FILE
		self.login_sleep_time = config.LOGIN_SLEEP_TIME

		# logger = logging.getLogger('JdLogin')
		# logger.setLevel(logging.INFO)
		# rh=logging.handlers.TimedRotatingFileHandler('log/jdlogin.log','D')
		# fm=logging.Formatter("%(asctime)s  %(levelname)s - %(message)s","%Y-%m-%d %H:%M:%S")
		# rh.setFormatter(fm)
		# logger.addHandler(rh)
		# self.infolog=logger.info
		# self.errorlog=logger.error

	def get_sess(self):
		return self.sess

	def get_cookies(self):
		return self.cookies

	# cookies 序列化到文件
	def save_cookies_to_file(self):
		try:
			with open(self.cookie_file, 'wb') as f:
				pickle.dump(self.cookies, f)
		except Exception as e:
			# self.errorlog("cookies save to file False %s", e)
			print (u"cookies save to file False %s", e)
		return


	# 从文件中反序列化到 cookies
	def load_cookies_to_file(self):
		try:
			with open(self.cookie_file, 'rb') as f:
				self.cookies = pickle.load(f)
		except Exception as e:
			# self.errorlog("cookies load to file False %s", e)
			print (u"cookies load to file False %s", e)
		return


	# 检查登录状态
	# 首先从文件中获取cookies 信息，然后查看该 cookies 是否有效，否则进行登录
	def check_login(self):
		self.load_cookies_to_file()
		resp = self.sess.get(
			'https://media.jd.com/gotoadv/goods', 
			headers = self.headers,
			cookies = self.cookies
		)
		tmp = bs4.BeautifulSoup(resp.text, "lxml").select('ul[class="nav navbar-nav navbar-right hidden-sm"]')
		if ( len(tmp) < 1 ):
			if not self.login_by_QR():
				return False
		return True

	def showImage(self, filename):
		osName = platform.system()
		if osName == 'Windows':
			subprocess.Popen([filename], shell=True)
		elif osName == 'Linux':
			if HasCommand('gvfs-open'):
				subprocess.Popen(['gvfs-open', filename])
			elif HasCommand('shotwell'):
				subprocess.Popen(['shotwell', filename])
			else:
				raise
		elif osName == 'Darwin':
			subprocess.Popen(['open', filename])
		else:
			raise Exception('other system')

	
	def login_by_QR(self):
		# jd login by QR code
		try:
			print u'+++++++++++++++++++++++++++++++++++++++++++++++++++++++'
			print u'{0} > 请打开京东手机客户端，准备扫码登陆:'.format(time.ctime())

			urls = (
				'https://passport.jd.com/new/login.aspx',
				'https://qr.m.jd.com/show',
				'https://qr.m.jd.com/check',
				'https://passport.jd.com/uc/qrCodeTicketValidation'
			)

			# step 1: open login page
			resp = self.sess.get(
				urls[0], 
				headers = self.headers
			)
			if resp.status_code != requests.codes.OK:
				print u'获取登录页失败: %u' % resp.status_code
				return False

			## save cookies
			for k, v in resp.cookies.items():
				self.cookies[k] = v
			

			# step 2: get QR image
			resp = self.sess.get(
				urls[1], 
				headers = self.headers,
				cookies = self.cookies,
				params = {
					'appid': 133,
					'size': 147,
					't': (long)(time.time() * 1000)
				}
			)
			if resp.status_code != requests.codes.OK:
				print u'获取二维码失败: %u' % resp.status_code
				return False

			## save cookies
			for k, v in resp.cookies.items():
				self.cookies[k] = v

			## save QR code
			image_file = 'qr.png'
			with open (image_file, 'wb') as f:
				for chunk in resp.iter_content(chunk_size=1024):
					f.write(chunk)
			
			## scan QR code with phone
			self.showImage(image_file)

			# step 3： check scan result
			## mush have
			self.headers['Host'] = 'qr.m.jd.com' 
			self.headers['Referer'] = 'https://passport.jd.com/new/login.aspx'

			# check if QR code scanned
			qr_ticket = None
			retry_times = 100
			while retry_times:
				retry_times -= 1
				resp = self.sess.get(
					urls[2],
					headers = self.headers,
					cookies = self.cookies,
					params = {
						'callback': 'jQuery%u' % random.randint(100000, 999999),
						'appid': 133,
						'token': self.cookies['wlfstk_smdl'],
						'_': (long)(time.time() * 1000)
					}
				)

				if resp.status_code != requests.codes.OK:
					continue

				n1 = resp.text.find('(')
				n2 = resp.text.find(')')
				rs = json.loads(resp.text[n1+1:n2])

				if rs['code'] == 200:
					print u'{} : {}'.format(rs['code'], rs['ticket'])
					qr_ticket = rs['ticket']
					break
				else:
					print u'{} : {}'.format(rs['code'], rs['msg'])
					time.sleep( self.login_sleep_time )
			
			if not qr_ticket:
				print u'二维码登陆失败'
				return False
			
			# step 4: validate scan result
			## must have
			self.headers['Host'] = 'passport.jd.com'
			self.headers['Referer'] = 'https://passport.jd.com/uc/login?ltype=logout'
			resp = self.sess.get(
				urls[3], 
				headers = self.headers,
				cookies = self.cookies,
				params = {'t' : qr_ticket },
			)
			print resp
			if resp.status_code != requests.codes.OK:
				print u'二维码登陆校验失败: %u' % resp.status_code
				return False
			
			## login succeed
			self.headers['P3P'] = resp.headers.get('P3P')
			for k, v in resp.cookies.items():
				self.cookies[k] = v
			
			print u'登陆成功'
			self.save_cookies_to_file()
			return True
		
		except Exception as e:
			print u'Exp:', e
			raise

		return False



	# 持久化保持登录状态
	def persistence_login_by_webdrive(self):
		# 使用webdrive登录MJD
		osName = platform.system()
		if osName == 'Windows':
			driver = webdriver.Chrome('./chromedriver.exe')
		else:
			driver = webdriver.Chrome('./chromedriver')

		# 京东移动页面登录
		driver.get('https://passport.jd.com/new/login.aspx?ReturnUrl=http%3A%2F%2Fmedia.jd.com%2Fgotoadv%2Fgoods')

		# 等待登录完成页
		element = WebDriverWait(driver, 1200).until(
			EC.presence_of_element_located((By.CLASS_NAME, "navbar-header"))
		)

		# 从 driver 获取 cookies 
		cookie_list = driver.get_cookies()
		# print cookie_list
		# 读取有用的 cookies 信息
		cookie_dict = {}
		for cookie in cookie_list:
			if cookie.has_key('name') and cookie.has_key('value'):
				cookie_dict[cookie['name']] = cookie['value']
		self.cookies = cookie_dict
		self.save_cookies_to_file()


		urls = [
			'https://media.jd.com/gotoadv/goods?pageSize=50',
			'https://media.jd.com/gotoadv/goods?pageIndex=1&pageSize=50&property=&sort=&goodsView=list&adownerType=g&pcRate=&wlRate=&category1=&category=&category3=&condition=1&fromPrice=&toPrice=&keyword=&price=PC',
			'https://media.jd.com/gotoadv/goods?pageIndex=&pageSize=10&property=&sort=&goodsView=list&adownerType=g&pcRate=&wlRate=&category1=9987&category=&category3=&condition=1&fromPrice=&toPrice=&keyword=',
			'https://media.jd.com/gotoadv/goods?pageIndex=&pageSize=10&property=&sort=&goodsView=list&adownerType=g&pcRate=&wlRate=&category1=670&category=&category3=&condition=1&fromPrice=&toPrice=&keyword=',
			'https://media.jd.com/gotoadv/goods?pageIndex=&pageSize=10&property=&sort=&goodsView=list&adownerType=g&pcRate=&wlRate=&category1=6728&category=&category3=&condition=1&fromPrice=&toPrice=&keyword=',
			'https://media.jd.com/gotoadv/goods?pageIndex=&pageSize=10&property=&sort=&goodsView=list&adownerType=g&pcRate=&wlRate=&category1=1318&category=&category3=&condition=1&fromPrice=&toPrice=&keyword=',
		]
		driver.set_window_size(400, 400)
		driver.set_window_position(x=0, y=0)
		while True:
			ii = random.randint(0, len(urls)-1)
			driver.get(urls[ii])
			time.sleep(10)
			# 从 driver 获取 cookies 
			cookie_list = driver.get_cookies()
			# 读取有用的 cookies 信息
			cookie_dict = {}
			for cookie in cookie_list:
				if cookie.has_key('name') and cookie.has_key('value'):
					cookie_dict[cookie['name']] = cookie['value']
			self.cookies = cookie_dict
			self.save_cookies_to_file()
			print u'[ 京东联盟后台 ] 写 cookies 然后休眠 ...'
			time.sleep(20)



def main(options):
	jdlogin = JdLogin()
	if options.persistence == True:
		print u'[ 京东联盟后台 ] 持久化保持登录状态'
		jdlogin.persistence_login_by_webdrive()



if __name__ == '__main__':
	# help message
	parser = argparse.ArgumentParser(description='京东联盟后台登录保持程序')
	parser.add_argument('-p', '--persistence', 
						help='持久化保持登录状态', action="store_true")
	options = parser.parse_args()
	print options
	main(options)

