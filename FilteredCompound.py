# -*- coding: utf-8 -*-
# 
# 过滤商品、劵信息，防止不必要的上传和采集操作
# xiangcy@jixunsoft.cn 2017-06-07
# 

import config

import re, os, time, sys, csv
import argparse
import requests
import urlparse
import ExistingCommodity
import AnalyticalURL

reload(sys)
sys.setdefaultencoding('utf-8')

# get function name
FuncName = lambda n=0: sys._getframe(n + 1).f_code.co_name
# 改变目录
os.chdir(sys.path[0])

class FilteredCompound(object):
	def __init__(self):
		self.existing_skuid_uniq_file = config.BASE_EXISTING_SKUID_UNIQ_FILE
		self.existing_coupons_uniq_file = config.BASE_EXISTING_COUPONS_UNIQ_FILE
		self.existing_compound_uniq_file = config.BASE_EXISTING_COMPOUND_UNIQ_FILE

		self.existingcommodity = ExistingCommodity.ExistingCommodity()
		self.analyticalurl = AnalyticalURL.AnalyticalURL()

		self.existing_skuid_uniq = []
		self.existing_coupons_uniq = []
		self.existing_compound_uniq = []


	def load_skuids(self):
		self.existing_skuid_uniq = self.existingcommodity.load_skuids()

	def get_skuids(self):
		if len(self.existing_skuid_uniq) < 1:
			self.load_skuids()
		return self.existing_skuid_uniq



	def load_coupons(self):
		self.existing_coupons_uniq = self.existingcommodity.load_coupons()

	def get_coupons(self):
		if len(self.existing_coupons_uniq) < 1:
			self.load_coupons()
		return self.existing_coupons_uniq



	def load_compound(self):
		self.existing_compound_uniq = self.existingcommodity.load_compound()

	def get_compound(self):
		if len(self.existing_compound_uniq) < 1:
			self.load_compound()
		return self.existing_compound_uniq



	def save_datas(self, datas, file_path):
		file = open(file_path, "wb")
		for data in datas:
			file.write( data + u"\n")
		file.close()
		return 


	def filtered(self, item_url, coupon_url):
		item_url = self.analyticalurl.get_real_item_url(item_url)
		coupon_url = self.analyticalurl.get_real_coupon_url(coupon_url)
		if item_url == None or coupon_url == None:
			return True

		# 获取 skuid key roleid
		skuid = re.findall(r"(\d+)", item_url)[0]
		tmp = re.findall(r'key\=(\w+)\&roleId\=(\d+)\&?', coupon_url)[0]
		key = tmp[0]
		roleid = tmp[1]
		# 判断是否已入库
		if len(skuid) > 0 and len(key) > 0 and len(roleid) > 0:
			# 过滤通用卷
			if key in ['9b1fe593e9f14c57a8bd158086c2ac82']:
				return True
			tmp = str(skuid) + str(key) + str(roleid)
			if tmp in self.existing_compound_uniq:
				return True
			else:
				return False



	def filtered_from_file(self, file_path):
		self.load_compound()
		items = []
		csvfile = file(file_path, 'rb')
		csv.field_size_limit(10000)
		reader = csv.reader(csvfile)
		for itemurl, mjurl in reader:
			if self.filtered(itemurl, mjurl):
				continue
			else:
				items.append(item)
		items = list(set(items))
		return items



	def filtered_from_data(self, datas):
		self.load_compound()
		items = []
		for item in datas:
			if self.filtered(item['itemurl'], item['mjurl']):
				continue
			else:
				items.append(item)
		return items







