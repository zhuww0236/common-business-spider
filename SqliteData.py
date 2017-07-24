# -*- coding: utf-8 -*-
# 使用 sqlite3 读写数据
# xiangcy@jixunsoft.cn
# 2017-06-12

import config

import re, os, time, sys
import sqlite3
import pickle
import hashlib
import AnalyticalURL

reload(sys)
sys.setdefaultencoding('utf-8')

# get function name
FuncName = lambda n=0: sys._getframe(n + 1).f_code.co_name


class SqliteData(object):
	def __init__(self):
		self.coupons_databases_path = './db/coupons.db'
		self.items_databases_path = './db/items.db'
		self.analyticalurl = AnalyticalURL.AnalyticalURL()
		self.create_table_coupons()



	# 新建表
	def create_table_coupons(self):
		conn = sqlite3.connect(self.coupons_databases_path)
		cursor = conn.cursor()
		# 检查表不存在即创建
		try:  
			create_tb_cmd='''
				CREATE TABLE IF NOT EXISTS coupons 
				(
					coupon_id CHAR(50) PRIMARY KEY NOT NULL, 
					coupon_key CHAR(32) NOT NULL, 
					coupon_roleid INT NOT NULL, 
					coupon_status INT NOT NULL, 
					coupon_money INT NOT NULL, 
					coupon_restrict INT NOT NULL, 
					coupon_url TEXT NOT NULL, 
					coupon_startTime CHAR(19) NOT NULL, 
					coupon_endTime CHAR(19) NOT NULL, 
					createTime CHAR(19) NOT NULL, 
					updateTime CHAR(19) NOT NULL
				);
			'''
			conn.execute(create_tb_cmd)
			return True
		except:
			print "Create table failed"
			return False



	# 从库读取劵信息
	def read_coupons(self, url):
		tmp = self.analyticalurl.get_key_and_roleid_new(url)
		if tmp == None:
			print u'劵解析失败: key, roleid 无法获取。' + url
			return False
		key = tmp['key']
		roleid = tmp['roleid']
		coupon_id = str(key) + str(roleid)

		conn = sqlite3.connect(self.coupons_databases_path)
		cursor = conn.cursor()
		coupon_id = str(key) + str(roleid)
		# print tmp, key, roleid, coupon_id, url
		try:  
			cursor.execute('select coupon_id, coupon_key, coupon_roleid, coupon_status, coupon_money, coupon_restrict, coupon_url, coupon_startTime, coupon_endTime, createTime, updateTime from coupons where coupon_id=\'' + coupon_id + '\'')
			values = cursor.fetchall()
			cursor.close()
			conn.close()
			return values
		except Exception, e:
			cursor.close()
			conn.close()
			print "select data failed : %s", e
			return []



	# 写库
	def write_coupons(self, coupon_info):
		# 先判断是否已经入库
		tmp = self.analyticalurl.get_key_and_roleid_new(coupon_info['url'])
		if tmp == None:
			print u'劵解析失败: key, roleid 无法获取。' + coupon_info['url']
			return False
		key = tmp['key']
		roleid = tmp['roleid']
		coupon_id = str(key) + str(roleid)
		createTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
		updateTime = createTime
		tmp = self.read_coupons(coupon_info['url'])

		if len(tmp) > 0:
			# 已经入库，更新
			return self.update_coupons(coupon_info)
		else:
			# 没有入库，新增
			return self.add_coupons(coupon_info)



	# 新增劵信息到库
	def add_coupons(self, coupon_info):
		conn = sqlite3.connect(self.coupons_databases_path)
		cursor = conn.cursor()
		# 写库
		tmp = self.analyticalurl.get_key_and_roleid_new(coupon_info['url'])
		if tmp == None:
			print u'劵解析失败: key, roleid 无法获取。' + coupon_info['url']
			return False
		key = tmp['key']
		roleid = tmp['roleid']
		coupon_id = str(key) + str(roleid)
		createTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
		updateTime = createTime
		try:  
			cursor.execute('insert into coupons (coupon_id, coupon_key, coupon_roleid, coupon_status, coupon_money, coupon_restrict, coupon_url, coupon_startTime, coupon_endTime, createTime, updateTime) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (coupon_id, key, roleid, coupon_info['status'], coupon_info['value'], coupon_info['restrict'], coupon_info['url'], coupon_info['startTime'], coupon_info['endTime'], createTime, updateTime))
			cursor.rowcount
			cursor.close()
			conn.commit()
			conn.close()
		except Exception, e:
			cursor.close()
			conn.close()
			print "insert data failed : %s", e
			return False
		return True



	# 更新劵信息到库
	def update_coupons(self, coupon_info):
		conn = sqlite3.connect(self.coupons_databases_path)
		cursor = conn.cursor()
		# 写库
		tmp = self.analyticalurl.get_key_and_roleid_new(coupon_info['url'])
		if tmp == None:
			print u'劵解析失败: key, roleid 无法获取。' + coupon_info['url']
			return False
		coupon_id = str(tmp['key']) + str(tmp['roleid'])
		updateTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
		try:
			cursor.execute('UPDATE coupons SET coupon_status=?, coupon_money=?, coupon_restrict=?, coupon_startTime=?, coupon_endTime=?, updateTime=? WHERE coupon_id=?', (coupon_info['status'], coupon_info['value'], coupon_info['restrict'], coupon_info['startTime'], coupon_info['endTime'], updateTime, coupon_id))
			cursor.rowcount
			cursor.close()
			conn.commit()
			conn.close()
		except Exception, e:
			cursor.close()
			conn.close()
			print "update data failed : %s", e
			return False
		return True



	# 新建商品表
	def create_table_items(self):
		conn = sqlite3.connect(self.items_databases_path)
		cursor = conn.cursor()
		# 检查表不存在即创建
		try:  
			create_tb_cmd='''
				CREATE TABLE IF NOT EXISTS items 
				(
					skuid INTEGER PRIMARY KEY NOT NULL,
					createTime CHAR(19) NOT NULL, 
					updateTime CHAR(19) NOT NULL,
					data_md5 CHAR(32) NOT NULL,
					data TEXT NOT NULL
				);
			'''
			conn.execute(create_tb_cmd)
			return True
		except:
			print "Create items table failed"
			return False



	# 从库读取劵信息
	def read_items(self, skuid):
		conn = sqlite3.connect(self.items_databases_path)
		cursor = conn.cursor()
		try:  
			cursor.execute('select skuid, createTime, updateTime, data_md5, data from items where skuid=\'' + skuid + '\'')
			values = cursor.fetchall()
			cursor.close()
			conn.close()
			# 反序列化
			data = pickle.loads(values[4])
			values[4] = data
			return values
		except Exception, e:
			cursor.close()
			conn.close()
			print "select itmes data failed : %s", e
			return []



	# 写库
	def write_items(self, skuid, item_info):
		# 先判断是否已经入库
		if item_info == None or len(item_info) < 1 or skuid < 1:
			return False
		tmp = self.read_items(skuid)
		if len(tmp) > 0:
			# 已经入库，更新
			return self.update_coupons(skuid, item_info)
		else:
			# 没有入库，新增
			return self.add_coupons(skuid, item_info)



	# 新增劵信息到库
	def add_items(self, skuid, item_info):
		conn = sqlite3.connect(self.items_databases_path)
		cursor = conn.cursor()
		# 写库
		if item_info == None or len(item_info) < 1 or skuid < 1:
			return False
		data = pickle.dumps(item_info)
		data_md5 = hashlib.new("md5", data).hexdigest()
		createTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
		updateTime = createTime
		try:  
			cursor.execute('insert into items (skuid, createTime, updateTime, data_md5, data) values (?, ?, ?, ?, ?)', (skuid, createTime, updateTime, data_md5, data))
			cursor.rowcount
			cursor.close()
			conn.commit()
			conn.close()
		except Exception, e:
			cursor.close()
			conn.close()
			print "insert items data failed : %s", e
			return False
		return True



	# 更新劵信息到库
	def update_items(self, skuid, item_info):
		conn = sqlite3.connect(self.items_databases_path)
		cursor = conn.cursor()
		# 写库
		if item_info == None or len(item_info) < 1 or skuid < 1:
			return False
		data = pickle.dumps(item_info)
		data_md5 = hashlib.new("md5", data).hexdigest()
		updateTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
		try:
			cursor.execute('UPDATE items SET updateTime=?, data_md5=?, data=? WHERE skuid=?', (updateTime, data_md5, data, skuid))
			cursor.rowcount
			cursor.close()
			conn.commit()
			conn.close()
		except Exception, e:
			cursor.close()
			conn.close()
			print "update items data failed : %s", e
			return False
		return True

