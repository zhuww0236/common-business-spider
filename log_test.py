# -*- coding: utf-8 -*-

# 爬取京东隐藏优惠券

import config

import bs4
import requests
import re, os, time, sys, platform
import logging, logging.handlers
import argparse

import MjdLogin

import pickle, csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


reload(sys)
sys.setdefaultencoding('utf-8')

# get function name
FuncName = lambda n=0: sys._getframe(n + 1).f_code.co_name
# 改变目录
os.chdir(sys.path[0])


def get_driver_cookies(driver, file):
	# 从 driver 获取 cookies 
	cookie_list = driver.get_cookies()
	# print cookie_list
	# 读取有用的 cookies 信息
	cookie_dict = {}
	for cookie in cookie_list:
		if cookie.has_key('name') and cookie.has_key('value'):
			cookie_dict[cookie['name']] = cookie['value']
	save_cookies_to_file(cookie_dict, file)


# cookies 序列化到文件
def save_cookies_to_file(cookies, file):
	try:
		with open(file, 'wb') as f:
			pickle.dump(cookies, f)
	except Exception as e:
		print "cookies save to file False %s", e


# 从文件中反序列化到 cookies
def load_cookies_to_file(file):
	cookies = None
	try:
		with open(file, 'rb') as f:
			cookies = pickle.load(f)
	except Exception as e:
		print "cookies load to file False %s", e
	return cookies

'''
# 使用webdrive登录MJD
osName = platform.system()
if osName == 'Windows':
	driver = webdriver.Chrome('./chromedriver.exe')
else:
	driver = webdriver.Chrome('./chromedriver')
# 京东移动页面登录
driver.get('https://plogin.m.jd.com/user/login.action?appid=100&kpkey=')
time.sleep(5)
# print u'输入账号'
driver.find_element_by_id("username").send_keys('redrum0003')
time.sleep(1)
driver.find_element_by_id("password").send_keys('Rg35D7jL2fmWhF-T')

# 等待登录完成页
element = WebDriverWait(driver, 1200).until(
	EC.presence_of_element_located((By.CLASS_NAME, "jd-search-icon-logined"))
)
get_driver_cookies(driver, './cookies/cookies_test_01.txt')

# 页面2
time.sleep(1)
driver.get('https://shop.m.jd.com/my/follows')
time.sleep(5)
get_driver_cookies(driver, './cookies/cookies_test_02.txt')

# 页面3
time.sleep(1)
driver.get('http://coupon.m.jd.com/coupons/show.action?key=4a12e51d123443978514f622ef6c5f86&roleId=6299565&to=uways.jd.com')
time.sleep(5)
get_driver_cookies(driver, './cookies/cookies_test_03.txt')

# 页面4
time.sleep(1)
driver.get('http://coupon.m.jd.com/coupons/show.action?key=bd6f6c8954574936b4792ee467010100&roleId=6337274&to=mall.jd.com/')
time.sleep(5)
get_driver_cookies(driver, './cookies/cookies_test_04.txt')

# 关闭 driver
driver.quit()
'''
headers = {
	'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
	'ContentType': 'text/html; charset=utf-8',
	'Accept-Encoding':'gzip, deflate, sdch',
	'Accept-Language':'zh-CN,zh;q=0.8',
	'Connection' : 'keep-alive',
}
session = requests.Session()
cookies = load_cookies_to_file('./cookies/cookies_test_01.txt')
response = session.get(
	'https://home.m.jd.com/myJd/newhome.action', 
	headers = headers,
	cookies = cookies
)
cookies_d = requests.utils.dict_from_cookiejar(response.cookies)
print u'header ----------'
print response.headers
print u'-----------------'
print u'cookies ----------'
print cookies_d
print u'-----------------'
# for cookie in response.cookies:
# 	# if cookie.has_key('name') and cookie.has_key('value'):
# 	print cookie
response = session.get(
	'http://coupon.m.jd.com/coupons/show.action?key=4a12e51d123443978514f622ef6c5f86&roleId=6299565&to=uways.jd.com'
)
cookies_d = requests.utils.dict_from_cookiejar(response.cookies)
print u'header ----------'
print response.headers
print u'-----------------'
print u'cookies ----------'
print cookies_d
print u'-----------------'

response = session.get(
	'http://coupon.m.jd.com/coupons/show.action?key=bd6f6c8954574936b4792ee467010100&roleId=6337274&to=mall.jd.com/'
)
cookies_d = requests.utils.dict_from_cookiejar(response.cookies)
print u'header ----------'
print response.headers
print u'-----------------'
print u'cookies ----------'
print cookies_d
print u'-----------------'

