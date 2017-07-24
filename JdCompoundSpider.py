# -*- coding: utf-8 -*-

import config

import re, os, time, sys
import argparse
import requests
import urllib2
import csv

import JdCompoundSpiderClass
import ExistingCommodity
import FilteredCompound

reload(sys)
sys.setdefaultencoding('utf-8')

# get function name
FuncName = lambda n=0: sys._getframe(n + 1).f_code.co_name
# 改变目录
os.chdir(sys.path[0])


def spider_main(conupons_channel_list):
	jdcompoundspiderclass = JdCompoundSpiderClass.JdCompoundSpiderClass()
	filteredcompound = FilteredCompound.FilteredCompound()
	existingcommodity = ExistingCommodity.ExistingCommodity()

	for channel in conupons_channel_list:
		if len(channel) < 1:
			continue

		print u'更新缓存'
		existingcommodity.get_data()
		print u'开始采集：[ %s ]  渠道：[ %s ] ==============' %(channel['title'], channel['channel'])


		# 从文件获取需要采集的目标
		conupons = []
		csvfile = file(channel['file_path'], 'rb')
		csv.field_size_limit(10000)
		reader = csv.reader(csvfile)
		for itemurl, mjurl in reader:
			item = {
				'itemurl': itemurl,
				'mjurl': mjurl
			}
			conupons.append(item)


		w_conupons_num = len(conupons)
		w_conupons_new_num = w_conupons_num

		if channel['title'] != '京推推' and channel['title'] != '第三方':

			# 去重过滤
			conupons_new = filteredcompound.filtered_from_data(conupons)
			w_conupons_new_num = len(conupons_new)
		else:
			conupons_new = conupons

		is_null = 0
		not_null = 0
		print u' 总数: [ ' + str(w_conupons_num) + ' ] 待采集数量: [ ' + str(w_conupons_new_num) + ' ]'
		i = 0
		for conupon in conupons_new:
			# # 只采集前一千张劵
			# i = i + 1
			# if i > 1000:
			# 	break

			jdcompoundspiderclass.get_info(conupon['itemurl'], conupon['mjurl'], channel['channel'])
			time.sleep(0.2)



def main(options):
	conupons_channel_list = [
		# {'title': '招商',	'tag': 'zs',	'channel': '1', 'file_path': './csv/jd_conupons_channel_1_uniq.csv'},
		{'title': '小草联盟',	'tag': 'xclm',	'channel': '3', 'file_path': './csv/json_spider_01.csv'},
		{'title': '小豚鼠',	'tag': 'xts',	'channel': '4', 'file_path': './csv/json_spider_02.csv'},
		{'title': '友邻',	'tag': 'yl',	'channel': '0', 'file_path': './csv/json_spider_yl.csv'},
		{'title': '京推推',	'tag': 'jtt',	'channel': '0', 'file_path': './csv/json_spider_04.csv'},
		# {'title': '第三方',	'tag': 'dsf',	'channel': '0', 'file_path': './csv/jd_conupons_channel_0_uniq.csv'},
	]
	if len(options) < 1:
		spider_main(conupons_channel_list)
	else:
		tmp = []
		for channel_tag in options:
			for conupons_channel in conupons_channel_list:
				if channel_tag == conupons_channel['tag']:
					tmp.append(conupons_channel)
					break
		if len(tmp) < 1:
			print u'--------------------请从以下渠道中选择：'
			for conupons_channel in conupons_channel_list:
				print conupons_channel['tag'] + u' (' + conupons_channel['title'] + u')'
			print u'------------------------------------'
			return
		else:
			spider_main(tmp)


if __name__ == '__main__':
	# help message
	parser = argparse.ArgumentParser(description='京东商品、劵混合采集程序')		
	parser.add_argument('-c', '--channel', type=str, 
						dest='channel', 
						action='append', default=[],
						help='渠道名称, 可多选。不选择时采集所有渠道  eg: -cxts -cxclm -cyl')			
	options = parser.parse_args()
	print options
	channel = []
	if len(options.channel) > 0:
		for channel_tag in options.channel:
			channel.append(channel_tag)
	main(channel)

