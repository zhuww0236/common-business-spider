# -*- coding: utf-8 -*-

import config

import requests
import re, os, time, sys
import logging, logging.handlers
import json, csv
import argparse
import commands

reload(sys)
sys.setdefaultencoding('utf-8')

# get function name
FuncName = lambda n=0: sys._getframe(n + 1).f_code.co_name


class UploadData(object):
	def __init__(self):

		self.upload_host = ''
		self.timeout_upload_connect = config.TIMEOUT_UPLOAD_CONNECT
		self.timeout_upload_request = config.TIMEOUT_UPLOAD_REQUEST
		self.base_csv_file = ''
		self.base_uniq_csv_file = ''
		self.base_csv_limit = config.BASE_CSV_LIMIT
		self.only_update = False

		# logger = logging.getLogger('uploadData')
		# logger.setLevel(logging.INFO)
		# rh=logging.handlers.TimedRotatingFileHandler('log/uploaddata.log', 'D')
		# fm=logging.Formatter("%(asctime)s  %(levelname)s - %(message)s","%Y-%m-%d %H:%M:%S")
		# rh.setFormatter(fm)
		# logger.addHandler(rh)
		# self.infolog=logger.info
		# self.errorlog=logger.error

	# 设置只上传，不做文件排重
	def set_only_update(self):
		self.only_update = True

	# 设置原始缓存文件路径
	def set_csv_file_path(self, file_path):
		self.base_csv_file = file_path



	# 设置排重缓存文件路径
	def set_csv_uniq_file_path(self, file_path):
		self.base_uniq_csv_file = file_path



	# 设置上传接口URL
	def set_upload_host(self, url):
		self.upload_host = url



	# 清空原始缓存文件
	def clean_csv(self):
		try:
			csvfile = file(self.base_csv_file, 'wb')
			csvfile.close()
			return True
		except Exception, e:
			print u'清理文件失败 %s' %(e)
			# self.errorlog('清理文件失败 %s' %(e))
			return False



	# 检查设置是否全部正确
	def check_config(self):
		if len(self.base_csv_file) < 1:
			print u'base_csv_file is null'
			# self.errorlog(u'base_csv_file is null')
			return False
		elif len(self.base_uniq_csv_file) < 1:
			print u'base_uniq_csv_file is null'
			# self.errorlog(u'base_uniq_csv_file is null')
			return False
		elif len(self.upload_host) < 1:
			print u'upload_host is null'
			# self.errorlog(u'upload_host is null')
			return False
		return True



	# 输出到文件暂存
	def save_items_to_file(self, items):
		if self.check_config() == False:
			return False
		if len(items) < 1:
			print u'items is null'
			# self.errorlog(u'items is null')
			return False
		data = []
		for item in items:
			tmp = (
				item['id'],
				item['title'],
				item['img'],
				item['price']['pc'],
				item['price']['wx'],
				item['commissionShare']['pc'],
				item['commissionShare']['wx'],
				item['commission']['pc'],
				item['commission']['wx'],
				item['count30Days'],
				item['comm30Days'],
				item['startTime'],
				item['endTime'],
				item['adownerType'],
				item['category1'],
				item['category']
			)
			data.append(tmp)
		try:
			csvfile = file(self.base_csv_file, 'ab')
			writer = csv.writer(csvfile)
			writer.writerows(data)
			csvfile.close()
		except Exception, e:
			print u'{0} : {1}'.format(FuncName(), e)
			# self.errorlog('{0} : {1}'.format(FuncName(), e))
		# self.infolog('写入暂存文件完成')
		return



	# 上传数据
	def upload_json(self, items):
		if self.check_config() == False:
			return False
		if len(items) < 1:
			print u'items is null'
			# self.errorlog(u'items is null')
			return False
		# 上传数据到接口
		try:
			r = requests.post(
				self.upload_host, 
				json=items,
				timeout = (self.timeout_upload_connect, self.timeout_upload_request)
			);
		except Exception, e:
			print u'{0} : {1}'.format(FuncName(), e)
			# self.errorlog('{0} : {1}'.format(FuncName(), e))
		# self.infolog(r)
		return



	# 一次性上传所有数据
	def upload_json_whole(self):
		if self.check_config() == False:
			return False

		if self.only_update == False:
			# 通过命令行对CSV文件做排重
			command_str = "cat %s | sort | uniq > %s" %(self.base_csv_file, self.base_uniq_csv_file)
			status, output = commands.getstatusoutput(command_str)
			if len(output) > 0:
				print u'排重文件失败: %s' %(output)
				# self.errorlog('排重文件失败: %s' %(output))
				print u'停止上传'
				# self.errorlog('停止上传')
				return False
			else:
				print u'排重文件成功: %s' %(output)
				# self.errorlog('排重文件成功: %s' %(output))

		# 读取排重后的CSV文件，以每次1000行上传数据
		# 读取数据
		items = []
		csv.field_size_limit(config.BASE_CSV_LIMIT)
		with open(self.base_uniq_csv_file, 'rb') as f:
			reader = csv.reader(f)
			for line in reader:
				try:
					print reader.line_num
					item = {
						'img': line[2],
						'id': line[0],
						'title': line[1],
						'price': {'pc': line[3], 'wx': line[4]},
						'commissionShare': {'pc': line[5], 'wx': line[6]},
						'commission': {'pc': line[7], 'wx': line[8]},
						'count30Days': line[9],
						'comm30Days': line[10],
						'startTime': line[11],
						'endTime': line[12],
						'adownerType': line[13],
						'category1': line[14],
						'category': line[15]
					}
				except Exception, e:
					continue
				items.append(item)
				# 达到指定的数量即上传
				if len(items) >= self.base_csv_limit:
					# 上传数据到接口
					self.upload_json(items)
					items = []
		# 上传剩余数据
		if len(items) > 0:
			# 上传数据到接口
			self.upload_json(items)
			items = []
		return
