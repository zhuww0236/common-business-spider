# -*- coding: utf-8 -*-

import config

import bs4
import requests
import re, os, time, sys
import logging, logging.handlers
import argparse

import JdGoodsPage
import JdLogin
import UploadData
import JdItemsPage

reload(sys)
sys.setdefaultencoding('utf-8')

# get function name
FuncName = lambda n=0: sys._getframe(n + 1).f_code.co_name
# 改变目录
os.chdir(sys.path[0])


class goodsItemsSpiderWhole(object):
	def __init__(self):
		
		self.sess = object
		self.cookies = {}
		self.finish = False
		self.sleep_time = config.SLEEP_TIMEPAGE_DONE
		self.max_page = config.BASE_MAX_PAGE
		self.options_max_page = 0

		logger = logging.getLogger('goodsItemsSpiderWholeLogger')
		logger.setLevel(logging.INFO)
		rh=logging.FileHandler('log/goodsitemsspiderwhole.log')
		fm=logging.Formatter("%(asctime)s  %(levelname)s - %(message)s","%Y-%m-%d %H:%M:%S")
		rh.setFormatter(fm)
		logger.addHandler(rh)
		self.infolog=logger.info
		self.errorlog=logger.error

		self.jdgoodspage = JdGoodsPage.JdGoodsPage()
		self.jdlogin = JdLogin.JdLogin()
		self.uploaddata = UploadData.UploadData()
		self.uploaddata.set_csv_file_path(config.BASE_CSV_FILE)
		self.uploaddata.set_csv_uniq_file_path(config.BASE_CSV_UNIQ_FILE)
		self.uploaddata.set_upload_host(config.BASE_UPLOAD_HOST)


	def set_options_max_page(self, max_page):
		if max_page > 0:
			self.options_max_page = max_page


	def jd_login(self):
		if self.jdlogin.check_login():
			self.sess = self.jdlogin.get_sess()
			self.cookies = self.jdlogin.get_cookies()
			return True
		else:
			return False



	def good_page(self, skuid):
		self.jdgoodspage.set_sess(self.sess)
		self.jdgoodspage.set_cookies(self.cookies)
		url = 'https://media.jd.com/gotoadv/goods?pageIndex=&pageSize=10&property=&sort=&adownerType=&pcRate=&wlRate=&category=&category1=0&condition=0&fromPrice=&toPrice=&goodsView=list&keyword=' + str(skuid)
		return self.jdgoodspage.goods_page(url)



	def goods_page(self, url):
		self.jdgoodspage.set_sess(self.sess)
		self.jdgoodspage.set_cookies(self.cookies)
		items = []
		items = self.jdgoodspage.goods_page(url)
		print ('商品数: %d', len(items))
		self.infolog('商品数: %d', len(items))
		if len(items) < 1:
			self.finish = True
			return
		if len(items) < 50:
			self.finish = True

		try:
			self.uploaddata.save_items_to_file(items)
			time.sleep( self.sleep_time )
		except Exception, e:
			# self.errorlog('Exp2 {0} : {1}'.format(FuncName(), e))
			pass



	# 单个分类
	def goods_category(self, category):
		page_index = 0
		self.finish = False

		# 特殊分类设置最大采集页
		if category['category1'] == '9987':
			max_page = 50
		elif category['category1'] == '652':
			max_page = 50
		elif category['category1'] == '670':
			max_page = 50
		else:
			max_page = self.max_page
		# 参数传入值最优先
		if self.options_max_page > 0:
			max_page = self.options_max_page


		# 循环该分类下的页
		while page_index < max_page:
			page_index += 1
			if self.finish:
				return
			else:
				if category['adownerType'] == 'g':
					# 自营不过滤佣金比例
					wlRate = ''
				else:
					# 商家的只采用佣金比例在15%以上的
					wlRate = '15'
				url = 'https://media.jd.com/gotoadv/goods?pageIndex=' + str(page_index) + '&pageSize=50&property=' + category['property'] + '&sort=desc&adownerType=' + category['adownerType'] + '&pcRate=&wlRate=' + wlRate + '&category=&category1=' + category['category1'] + '&condition=1&fromPrice=&toPrice=&goodsView=list&keyword='

				if page_index == 1:
					self.infolog(url)
					pass
				self.infolog('页数: %d / %d' %(page_index, max_page))
				self.goods_page(url)
			# print u'page_index: %d , finish: %s' %(page_index, self.finish)
			if self.finish and page_index == 1:
				return 'category_finish'



	# 完整的分类
	def category_list(self, category1s):
		if self.uploaddata.clean_csv() == False:
			print u'清理文件失败'
			self.errorlog('清理文件失败')
			return False
		# 待采集的商品分类列表
		if len(category1s) > 0:
			goodsCategorys = []
			for tmp in category1s:
				goodsCategorys.append(str(tmp))
		else:
			goodsCategorys = [
				# '6144' # debug
				# '652', '670' # debug
				'173', '174', '175', '652', '670', '737', '911', '1315', '1316', '1318', '1319', '1320', 
				'1620', '1672', '1713', '4051', '4052', '4053', '5025', '5272', '5273', '6144', '6196', '6233', '6728', '6994', '9192', '9669', '9847', '9855', '9987', '11729', '12218', '12259', '12362', '12473'
			]
		tmpCategorys = []
		for categoryId in goodsCategorys:
			tmpCategorys.append({'adownerType': 'g', 'category1': categoryId, 'property': 'pcCommissionShare'})
			tmpCategorys.append({'adownerType': 'g', 'category1': categoryId, 'property': 'pcCommission'})
			tmpCategorys.append({'adownerType': 'g', 'category1': categoryId, 'property': 'inOrderCount30Days'})
			tmpCategorys.append({'adownerType': 'g', 'category1': categoryId, 'property': 'inOrderComm30Days'})
			tmpCategorys.append({'adownerType': 'p', 'category1': categoryId, 'property': 'pcCommissionShare'})
			tmpCategorys.append({'adownerType': 'p', 'category1': categoryId, 'property': 'pcCommission'})
			tmpCategorys.append({'adownerType': 'p', 'category1': categoryId, 'property': 'inOrderCount30Days'})
			tmpCategorys.append({'adownerType': 'p', 'category1': categoryId, 'property': 'inOrderComm30Days'})
		category_finish = {}
		for category in tmpCategorys:
			# 如果分类在标记的数组中，则跳过本次循环
			tmp = category['adownerType'] + category['category1']
			if tmp in category_finish.keys():
				self.infolog('跳过本次循环, 原因：分类在标记的数组中')
				continue
			print category
			# self.infolog(category)
			# 如果发现标记，则将分类存放在数组中
			if self.goods_category(category) == 'category_finish':
				category_finish[ category['adownerType'] + category['category1'] ] = 1



	# 一次性上传所有数据
	def upload_json_whole(self, onlyupdate):
		if onlyupdate == True:
			print u'只上传，不做文件排重'
			jd.infolog(u'只上传，不做文件排重')
			self.uploaddata.set_only_update()
		return self.uploaddata.upload_json_whole()



	# 采集分类
	def cj_by_category(self, category1, max_page):
		# TODO
		print u'采集分类'
		# jd.infolog('采集分类')
		pass

	# 采集单个商品
	def cj_by_skuid(self, skuid):
		print u'采集单个商品'
		# jd.infolog('采集单个商品')
		pass

	# 从文件列表中读取商品ID采集商品
	def cj_skuids(self, file_path):
		# TODO
		pass

def main(options):
	jd = goodsItemsSpiderWhole()

	print u'---------------------'
	# jd.infolog('---------------------')
	print u'采集开始'
	# jd.infolog('采集开始')
	if not jd.jd_login():
		return

	# 采集分类
	if options.onlyupdate == False and options.good == 0:
		jd.set_options_max_page(options.count)
		jd.category_list(options.category1)
		print u'采集结束'
		# jd.infolog(u'采集结束')

	if options.onlyupdate == True and options.good == 0:
		print u'开始上传数据'
		# jd.infolog(u'开始上传数据')
		jd.upload_json_whole(options.onlyupdate)
		print u'上传数据结束'
		# jd.infolog(u'上传数据结束')


	# 采集单个商品
	if options.good > 0:
		item = jd.good_page(str(options.good))
		# print item
		if len(item) > 0 :
			print u'商品ID: '+ str(options.good)
			JdItemsPageSpider = JdItemsPage.JdItemsPage()
			tmp = JdItemsPageSpider.items_page_pc('https://item.jd.com/' + str(options.good) + '.html')
			if tmp != False and tmp != None and len(tmp) > 0:
				item[0]['category1'] = tmp['category1']
			print u'开始上传数据'
			# jd.infolog(u'开始上传数据')
			jd.uploaddata.upload_json(item)
		print u'上传数据结束'
		# jd.infolog(u'上传数据结束')
		return


if __name__ == '__main__':
	# help message
	parser = argparse.ArgumentParser(description='京东联盟商品采集程序')		
	group = parser.add_mutually_exclusive_group()
	group.add_argument('-g', '--good', type=int, 
						help='京东商品ID', default=0)
	group.add_argument('-y', '--category1', type=int, 
						dest='category1', 
						action='append', default=[],
						help='京东分类ID, 可多选  eg: -y111 -y222 -y333')

	parser.add_argument('-c', '--count', type=int, 
						dest='count', 
						help='采集最大页数', default=0)
	parser.add_argument('-o', '--onlyupdate', 
						help='只上传，不做文件排重', action="store_true")


				
	options = parser.parse_args()
	print options
	main(options)

