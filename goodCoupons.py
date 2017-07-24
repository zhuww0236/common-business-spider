# -*- coding: utf-8 -*-

# 爬取京东隐藏优惠券

import config

import bs4
import requests
import re, os, time, sys
import logging, logging.handlers
import argparse

import JdCouponsPage
import MjdLogin
import UploadData



reload(sys)
sys.setdefaultencoding('utf-8')

# get function name
FuncName = lambda n=0: sys._getframe(n + 1).f_code.co_name
# 改变目录
os.chdir(sys.path[0])


class goodCoupons(object):
	def __init__(self):
		
		self.sess = object
		self.cookies = {}
		self.finish = ''
		self.force = False
		self.sleep_time = config.SLEEP_TIMEPAGE_DONE
		self.get_items_host = config.BASE_GET_ITEMS_HOST

		self.jdcouponspage = JdCouponsPage.JdCouponsPage()
		self.mjdlogin = MjdLogin.MjdLogin()
		self.uploaddata = UploadData.UploadData()
		self.uploaddata.set_csv_file_path(config.BASE_COUPONS_CSV_FILE)
		self.uploaddata.set_csv_uniq_file_path(config.BASE_SKUID_CSV_UNIQ_FILE)
		self.uploaddata.set_upload_host(config.BASE_COUPONS_CSV_UNIQ_FILE)



	def get_sess(self):
		return self.sess



	def get_cookies(self):
		return self.cookies



	def set_force(self, switch = False):
		self.force = switch



	def jd_login(self):
		if self.mjdlogin.check_login():
			self.sess = self.mjdlogin.get_sess()
			self.cookies = self.mjdlogin.get_cookies()
			return True
		else:
			return False



	def coupons_page(self, skuid, url):
		items = []
		self.jdcouponspage.set_sess(self.sess)
		self.jdcouponspage.set_cookies(self.cookies)
		self.jdcouponspage.set_force(self.force)
		items = self.jdcouponspage.coupons_page(skuid, url)
		# print items
		return items



	def goods_conupons(self, skuid, url):
		print skuid
		print url
		self.coupons_page(skuid, url)


	'''
	def conupons_list(self):
		goodsItems = self.get_conupons()

		if self.uploaddata.clean_csv() == False:
			print u'清理文件失败'
			self.errorlog('清理文件失败')
			return False

		tmpCategorys = []
		for itemId in goodsItems:
			tmpCategorys.append({'keyword': itemId})
		for category in tmpCategorys:
			print category
			self.goods_category(category)
	'''


	# 一次性上传所有数据
	def upload_json_whole(self):
		return self.uploaddata.upload_json_whole()



	# 获取需要采集的商品ID
	def get_items(self):
		r = requests.get(self.get_items_host)
		print r
		items = r.json()
		return items



def main(options):
	jd = goodCoupons()
	print u'采集开始'
	jd.infolog('采集开始')
	if not jd.jd_login():
		return

	# jd.conupons_list()
	print jd.coupons_page('10171645630', 'http://coupon.m.jd.com/coupons/show.action?key=3095180c3f024b3aabd1cc8edac1614b&roleId=6384720&to=mall.jd.com/')


	# print u'采集结束'
	# jd.infolog(u'采集结束')
	# print u'开始上传数据'
	# jd.infolog(u'开始上传数据')
	# jd.upload_json_whole()
	# print u'上传数据结束'
	# jd.infolog(u'上传数据结束')


if __name__ == '__main__':
	# help message
	parser = argparse.ArgumentParser(description='根据商品ID来采集商品信息')
	options = parser.parse_args()
	print options
	main(options)
