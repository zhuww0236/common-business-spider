# -*- coding: utf-8 -*-

import config

import bs4
import requests, requests.packages.urllib3
import re, os, time, sys
import logging, logging.handlers
import urlparse

requests.packages.urllib3.disable_warnings()
reload(sys)
sys.setdefaultencoding('utf-8')

class JdGoodsPage():

	def __init__(self):
		logger = logging.getLogger('JdGoodsPageLogger')
		logger.setLevel(logging.INFO)
		rh=logging.handlers.TimedRotatingFileHandler('log/jdgoodspage.log','D')
		fm=logging.Formatter("%(asctime)s  %(levelname)s - %(message)s","%Y-%m-%d %H:%M:%S")
		rh.setFormatter(fm)
		logger.addHandler(rh)
		self.infolog=logger.info
		self.errorlog=logger.error

		self.sess = object
		self.cookies = {}
		self.err_sleep_time = config.SLEEP_TIMEPAGE_ERR
		self.timeout_doogs_page_connect = config.TIMEOUT_DOOGS_PAGE_CONNECT
		self.timeout_doogs_page_request = config.TIMEOUT_DOOGS_PAGE_REQUEST

	def set_sess(self, sess):
		self.sess = sess

	def set_cookies(self, cookies):
		self.cookies = cookies

	def goods_page(self, url):
		return self.goods_page_v20170518(url)


	def goods_page_v20170518(self, url):
		rs = urlparse.urlparse(url)
		q = urlparse.parse_qs(rs.query)
		if 'adownerType' not in q:
			adowner_type = ''
		else:
			adowner_type = q['adownerType'][0]
		if 'category1' not in q:
			category1 = ''
		else:
			category1 = q['category1'][0]
		items = []
		try:
			resp = self.sess.get(
				url,
				cookies = self.cookies,
				timeout = (self.timeout_doogs_page_connect, self.timeout_doogs_page_request)
			)
		except Exception, e:
			self.errorlog('get goods page err : %s', e)
			pass

		try:
			# good page
			soup = bs4.BeautifulSoup(resp.text, "lxml")
			# 获取商品价格、佣金
			tbody = soup.find(class_='table-body')
			trs = tbody.find_all(class_='table-tr clearfix')
			# 校验列表是否有商品
			if len(trs) < 1:
				time.sleep( self.err_sleep_time )
				return []
			for tr in trs:
				# print tr
				# 商品图片
				img = tr.find(class_='fore2').find('img').get('src')
				# 商品ID
				skuid = re.findall(r"(\d+)", tr.find(class_='fore2').find('a').get('href'))[0]
				# 商品名称
				tmp = tr.find(class_='fore3').find('a').getText().replace(',', '').replace('/', '').replace('\n', ' ')
				title = tmp.strip()
				# 自营属性
				if adowner_type == '':
					try:
						tmp = tr.find(class_='fore3').find(class_='txt-wrap').find(class_='shop').find('a')
						if tmp == None:
							adowner_type = 'g'
						else:
							adowner_type = 'p'
					except Exception, e:
						adowner_type = ''
				# 商品价格
				tmp = tr.find(class_='fore4').find_all(class_='value')
				# price_pc = re.findall(r"(\d+\.\d+)", tmp[0].getText().replace(',', ''))[0]
				# price_wx = re.findall(r"(\d+\.\d+)", tmp[1].getText().replace(',', ''))[0]
				price_wx = re.findall(r"(\d+\.\d+)", tmp[0].getText().replace(',', ''))[0]
				# 商业佣金比例
				tmp = tr.find(class_='fore5').find_all(class_='value')
				commissionShare_pc = re.findall(r"(\d+\.\d+)", tmp[0].getText().replace(',', ''))[0]
				commissionShare_wx = re.findall(r"(\d+\.\d+)", tmp[1].getText().replace(',', ''))[0]
				# 商品佣金
				tmp = tr.find(class_='fore6').find_all(class_='value')
				commission_pc = re.findall(r"(\d+\.\d+)", tmp[0].getText().replace(',', ''))[0]
				commission_wx = re.findall(r"(\d+\.\d+)", tmp[1].getText().replace(',', ''))[0]
				# 30天引入订单
				count30Days = re.findall(r"(\d+)", tr.find(class_='fore7').find('p').getText().replace(',', ''))[0]
				# 30天累计支出佣金
				comm30Days = re.findall(r"(\d+\.\d+)", tr.find(class_='fore8').find('p').getText().replace(',', ''))[0]
				# 推广时间
				try:
					tgsj = re.findall(r"(\d{4}\-\d{2}\-\d{2})", tr.find(class_='fore9').getText())
					startTime = tgsj[0];
					endTime = tgsj[1];
				except Exception, e:
					startTime = time.strftime("%Y-%m-%d", time.localtime())
					endTime = time.strftime("%Y-12-31", time.localtime())
				item = {
					'img': img,
					'id': skuid,
					'title': title,
					'price': {'pc': '0', 'wx': price_wx},
					'commissionShare': {'pc': commissionShare_pc, 'wx': commissionShare_wx},
					'commission': {'pc': commission_pc, 'wx': commission_wx},
					'count30Days': count30Days,
					'comm30Days': comm30Days,
					'startTime': startTime,
					'endTime': endTime,
					'adownerType': adowner_type,
					'category1': category1,
					'category': ''
				}
				items.append(item)
		except Exception, e:
			self.errorlog('Soup err %s', e)
			pass
		return items
