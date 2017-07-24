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

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

requests.packages.urllib3.disable_warnings()
reload(sys)
sys.setdefaultencoding('utf-8')

class MjdLogin():

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
		self.cookie_file = config.BASE_MJD_COOKIE_FILE
		self.login_sleep_time = config.LOGIN_SLEEP_TIME

		logger = logging.getLogger('MjdLogin')
		logger.setLevel(logging.INFO)
		rh=logging.FileHandler('log/mjdlogin.log')
		fm=logging.Formatter("%(asctime)s  %(levelname)s - %(message)s","%Y-%m-%d %H:%M:%S")
		rh.setFormatter(fm)
		logger.addHandler(rh)
		self.infolog=logger.info
		self.errorlog=logger.error

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
			self.errorlog("mjd cookies save to file False %s", e)
			print (u"mjd cookies save to file False %s", e)
		return


	# 从文件中反序列化到 cookies
	def load_cookies_to_file(self):
		try:
			with open(self.cookie_file, 'rb') as f:
				self.cookies = pickle.load(f)
		except Exception as e:
			self.errorlog("mjd cookies load to file False %s", e)
			print (u"mjd cookies load to file False %s", e)
		return


	# 检查登录状态
	# 首先从文件中获取cookies 信息，然后查看该 cookies 是否有效，否则进行登录
	def check_login(self):
		self.load_cookies_to_file()
		resp = self.sess.get(
			'https://home.m.jd.com/myJd/newhome.action', 
			headers = self.headers,
			cookies = self.cookies
		)
		tmp = bs4.BeautifulSoup(resp.text, "lxml").select('div[class="wrap loginPage"]')
		if ( len(tmp) > 0 ):
			if not self.login_by_webdrive():
				return False
		return True



	def login_by_webdrive(self):
		# 使用webdrive登录MJD
		osName = platform.system()
		if osName == 'Windows':
			driver = webdriver.Chrome('./chromedriver.exe')
		else:
			driver = webdriver.Chrome('./chromedriver')

		# 京东移动页面登录
		driver.get('https://plogin.m.jd.com/user/login.action?appid=100&kpkey=')
		time.sleep(5)
		print u'输入账号'
		driver.find_element_by_id("username").send_keys(config.MJD_LOGIN_NAME)
		time.sleep(1)
		driver.find_element_by_id("password").send_keys(config.MJD_LOGIN_PASSWORD)

		# 等待登录完成页
		element = WebDriverWait(driver, 120).until(
			EC.presence_of_element_located((By.CLASS_NAME, "jd-search-icon-logined"))
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

		# 关闭 driver
		driver.quit()

		self.save_cookies_to_file()
		return True



	# 持久化保持登录状态
	def persistence_login_by_webdrive(self):
		# 使用webdrive登录MJD
		osName = platform.system()
		if osName == 'Windows':
			driver = webdriver.Chrome('./chromedriver.exe')
		else:
			driver = webdriver.Chrome('./chromedriver')

		# 京东移动页面登录
		driver.get('https://plogin.m.jd.com/user/login.action?appid=100&kpkey=')
		time.sleep(5)
		print u'输入账号'
		driver.find_element_by_id("username").send_keys(config.MJD_LOGIN_NAME)
		time.sleep(1)
		driver.find_element_by_id("password").send_keys(config.MJD_LOGIN_PASSWORD)

		# 等待登录完成页
		element = WebDriverWait(driver, 1200).until(
			EC.presence_of_element_located((By.CLASS_NAME, "jd-search-icon-logined"))
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
			'https://m.jd.com/',
			'https://home.m.jd.com/myJd/newhome.action',
			'https://coupon.m.jd.com/center/getCouponCenter.action',
			'https://item.m.jd.com/product/3133827.html',
			'https://item.m.jd.com/ware/view.action?wareId=11632712294',
			'https://item.m.jd.com/product/4499492.html',
		]
		driver.set_window_size(400, 400)
		driver.set_window_position(x=0, y=400)
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
			print u'写 cookies 然后休眠 ...'
			time.sleep(50)



def main(options):
	mjdlogin = MjdLogin()
	if options.persistence == True:
		print u'持久化保持登录状态'
		mjdlogin.persistence_login_by_webdrive()



if __name__ == '__main__':
	# help message
	parser = argparse.ArgumentParser(description='京东联盟商品采集程序')
	parser.add_argument('-p', '--persistence', 
						help='持久化保持登录状态', action="store_true")
	options = parser.parse_args()
	print options
	main(options)
