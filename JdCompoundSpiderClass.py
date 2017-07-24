# -*- coding: utf-8 -*-

import config

import re, os, time, sys
import argparse
import requests
import urllib2
from pprint import pprint
import csv
import logging, logging.handlers

import goodCoupons 
import JdItemsPage
import goodsItemsSpiderWhole
import AnalyticalURL
import ExistingCommodity

reload(sys)
sys.setdefaultencoding('utf-8')

# get function name
FuncName = lambda n=0: sys._getframe(n + 1).f_code.co_name
# 改变目录
os.chdir(sys.path[0])



class JdCompoundSpiderClass(object):
	def __init__(self):
		self.sess = object
		self.cookies = {}
		self.sleep_time = 0.3
		self.force = False

		self.JdCouponsSpider = goodCoupons.goodCoupons()
		self.JdItemsPageSpider = JdItemsPage.JdItemsPage()
		self.JdGoodsPageSpider = goodsItemsSpiderWhole.goodsItemsSpiderWhole()
		self.analyticalurl = AnalyticalURL.AnalyticalURL()
		self.existingcommodity = ExistingCommodity.ExistingCommodity()

		# 设置上传地址
		self.JdCouponsSpider.uploaddata.set_upload_host(config.BASE_UPLOAD_COUPONS_HOST)

		# 必要的登录
		self.JdCouponsSpider.jd_login()
		self.JdGoodsPageSpider.jd_login()

		# 读取已入库商品、劵信息
		self.compounds = self.existingcommodity.load_compound()



	def set_force(self, switch = False):
		self.force = switch


	def get_info(self, itemurl, mjurl, channel):
		item_url = self.analyticalurl.get_real_item_url(itemurl)
		conupon_url = self.analyticalurl.get_real_coupon_url(mjurl)
		# print item_url
		# print conupon_url
		if item_url == None:
			print u'商品地址解析失败 ' + itemurl + ' 跳过...'
			return u'商品地址解析失败'
		if conupon_url == None:
			print u'劵地址解析失败 ' + mjurl + ' 跳过...'
			return u'劵地址解析失败'

		# 获取 skuid key roleid
		skuid = re.findall(r"(\d+)", item_url)[0]
		tmp = re.findall(r'coupon\.m\.jd\.com\/coupons\/show\.action\?key\=(\w+)\&roleId\=(\d+)\&to\=', conupon_url)[0]
		key = tmp[0]
		roleid = tmp[1]
		if self.force == False:
			# 判断是否已入库
			if len(skuid) > 0 and len(key) > 0 and len(roleid) > 0:
				tmp = str(skuid) + str(key) + str(roleid)
				if tmp in self.compounds:
					print u'组合已入库，跳过...'
					return True

		# 采集卷信息
		couponInfo = self.JdCouponsSpider.coupons_page(skuid, conupon_url)
		# 采集商品信息
		self.JdItemsPageSpider.set_cookies(self.JdCouponsSpider.get_cookies())
		self.JdItemsPageSpider.set_sess(self.JdCouponsSpider.get_sess())
		tmp = self.JdItemsPageSpider.items_page_pc('https://item.jd.com/' + str(skuid) + '.html')
		# price = self.JdItemsPageSpider.items_page_m_get_price(skuid)
		if tmp != False and tmp != None and len(tmp) > 0:
			itemInfo = tmp
		else:
			itemInfo = None
		# 采集佣金商品信息
		tmp = self.JdGoodsPageSpider.good_page(skuid)
		print '采集佣金商品信息'
		if tmp != False and tmp != None and len(tmp) > 0:
			goodInfo = tmp[0]
		else:
			goodInfo = None
		if itemInfo != None and goodInfo != None:
			goodInfo['category1'] = itemInfo['category1']
			goodInfo['couponDto'] = couponInfo
			goodInfo['channel'] = channel
			goodInfo['adownerType'] = itemInfo['adownerType']
			goodInfo['images'] = itemInfo['images']
			goodInfo['linkSkuid'] = itemInfo['linkSkuid']
			# if price != '' and price != u'暂无报价':
			# 	goodInfo['price']['pc'] = price
			# 	goodInfo['price']['wx'] = price

		if goodInfo != None and itemInfo != None:
			tmp = []
			tmp.append(goodInfo)
			print u'商品 ' + str(skuid) + u' | 劵 ' + str(key) + u' ' + str(roleid)
			self.JdCouponsSpider.uploaddata.upload_json(tmp)
		elif goodInfo == None:
			print u'联盟后台无商品 ' + skuid + ' 跳过...'
			return u'联盟后台无商品'
		elif itemInfo == None:
			print u'商品分类采集失败 ' + skuid + ' 跳过...'
			return u'商品分类采集失败'
		return True


