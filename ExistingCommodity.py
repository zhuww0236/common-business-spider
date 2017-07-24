# -*- coding: utf-8 -*-
# 获取、更新已存在的商品、劵信息
# xiangcy@jixunsoft.cn
# 2017-06-13


import config

import re, os, time, sys, csv
import argparse
import requests
import urlparse

reload(sys)
sys.setdefaultencoding('utf-8')

# get function name
FuncName = lambda n=0: sys._getframe(n + 1).f_code.co_name
# 改变目录
os.chdir(sys.path[0])

class ExistingCommodity(object):
	def __init__(self):
		self.existing_skuid_uniq_file = config.BASE_EXISTING_SKUID_UNIQ_FILE
		self.existing_coupons_uniq_file = config.BASE_EXISTING_COUPONS_UNIQ_FILE
		self.existing_compound_uniq_file = config.BASE_EXISTING_COMPOUND_UNIQ_FILE



	def load_skuids(self):
		return self.load_datas(self.existing_skuid_uniq_file)


	def load_coupons(self):
		return self.load_datas(self.existing_coupons_uniq_file)


	def load_compound(self):
		return self.load_datas(self.existing_compound_uniq_file)


	def load_datas(self, file_path):
		datas = []
		csvfile = file(file_path, 'rb')
		csv.field_size_limit(10000)
		reader = csv.reader(csvfile)
		for data in reader:
			datas.append(data[0])
		csvfile.close()
		return datas



	def save_datas(self, datas, file_path):
		file = open(file_path, "wb")
		for data in datas:
			file.write( data + u"\n")
		file.close()
		return 



	def get_data(self):
		skuidList = []
		couponList = []
		compoundList = []
		r = requests.get(config.BASE_GET_COUPONS_UPDATE_HOST)
		conupons = r.json()
		for item in conupons['data']['couponList']:
			skuId = str(item['skuId'])
			skuidList.append(skuId)
			rs = urlparse.urlparse(item['url'])
			q = urlparse.parse_qs(rs.query)
			key = str(q['key'][0])
			roleId = str(q['roleId'][0])
			if 'key' in q and 'roleId' in q:
				if len(key) < 1 or len(roleId) < 1:
					continue
				else:
					couponList.append(key + roleId)
					compoundList.append(skuId + key + roleId)
			else:
				continue
		skuidList = list(set(skuidList))
		self.save_datas(skuidList, self.existing_skuid_uniq_file)
		couponList = list(set(couponList))
		self.save_datas(couponList, self.existing_coupons_uniq_file)
		compoundList = list(set(compoundList))
		self.save_datas(compoundList, self.existing_compound_uniq_file)



def main(options):
	existingc = ExistingCommodity()
	# if options.update:
	# 	existingc.get_data()
	existingc.get_data()
	skuids = existingc.load_skuids()
	coupons = existingc.load_coupons()
	compounds = existingc.load_compound()
	print 'skuid num: ' + str(len(skuids))
	print 'coupon num: ' + str(len(coupons))
	print 'compound num: ' + str(len(compounds))



if __name__ == '__main__':
	# help message
	parser = argparse.ArgumentParser(description='获取、更新已存在的商品、劵信息，目前可以获取三种信息：商品ID列表（ skuid ）、劵列表（ key + roleid ）、混合列表（ skuid + key + roleid ）')		
	parser.add_argument('-u', '--update', 
						help='从服务器更新已存在的商品、劵信息', action="store_true")				
	options = parser.parse_args()
	print options
	main(options)

