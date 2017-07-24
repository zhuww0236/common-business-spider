# -*- coding: utf-8 -*-
# 
# 获取QQ群的京东卷信息
# xiangcy@jixunsoft.cn 2017-05-11

import re
from wxpy import *
import JdCompoundSpiderClass
import time
import logging, logging.handlers

bot = Bot(cache_path=True)

jdcompoundspiderclass = JdCompoundSpiderClass.JdCompoundSpiderClass()
jdcompoundspiderclass.set_force(True)

logger = logging.getLogger('wxpy.api.bot')
logger.setLevel(logging.INFO)
rh=logging.handlers.TimedRotatingFileHandler('log/wxpy_api_bot.log','D')
fm=logging.Formatter("%(asctime)s  %(levelname)s - %(message)s","%Y-%m-%d %H:%M:%S")
rh.setFormatter(fm)
logger.addHandler(rh)
infolog=logger.info
errorlog=logger.error

def get_url_from_content(content):
	pattern = re.compile(r'((?:http|https)://[\w\-\.,@?^=%&:\/~\+#]+)')
	return re.findall(pattern, content)

# 过滤消息中的特殊字符，让链接地址能顺利提取
def filter_special_characters(content):
    tmp = content.replace('SKU', ' SKU').replace('sku', ' sku').replace(':', ' ').replace('：', ' ').replace('—', ' ').replace('--', ' ').replace('  ', ' ')
    tmp = tmp.replace('https //', 'https://').replace('http //', 'http://')
    tmp = tmp.replace('https://', ' https://').replace('http://', ' http://')
    tmp = tmp.replace('(', ' ').replace(')', ' ')
    return tmp


# 删除商品链接结尾的特殊字符
def filter_item_url(url):
	# 删除结尾 - 字符
	tmp = url.strip().lstrip().rstrip(',').rstrip('-')
	# 删除结尾 SKU:xxxx
	tmp2 = re.findall(r'((?i)SKU: ?\d+)$', tmp)
	if len(tmp2) > 0:
		tmp = tmp.replace(tmp2[0], '')
	# 删除结尾 SKUID:xxxx
	tmp2 = re.findall(r'((?i)SKU： ?\d+)$', tmp)
	if len(tmp2) > 0:
		tmp = tmp.replace(tmp2[0], '')
	return tmp



def check_url_type(urls, content):
	url_type = None

	# 兼容只有劵地址、商品地址是ID的情况
	if len(urls) == 1:
		tmp = re.findall(r'((?i)SKU[:|：]? *\d+)', content)
		if len(tmp) == 1:
			tmp2 = re.findall(r'(\d+)', tmp[0])
			url_type = {
				'conupon_url' : urls[0],
				'item_url' : u' https://item.m.jd.com/product/' + str(tmp2[0]) + u'.html'
			}
			return url_type

	if len(urls) != 2 and len(urls) != 3:
		return url_type

	if len(urls) == 3:
		tmp = []
		tmp.append(urls[1])
		tmp.append(urls[2])
		urls = None
		urls = tmp

	if len(re.findall(r'https?\:\/\/item\.jd\.com\/(\d+).html', urls[1])) > 0:
		url_type = {
			'conupon_url' : urls[0],
			'item_url' : filter_item_url(urls[1])
		}
		return url_type
	elif len(re.findall(r'https?\:\/\/union\-click\.jd\.com\/(\w+)', urls[1])) > 0:
		url_type = {
			'conupon_url' : urls[0],
			'item_url' : filter_item_url(urls[1])
		}
		return url_type
	elif len(re.findall(r'https?\:\/\/item\.m\.jd\.com\/ware\/view\.action\?wareId\=(\d+)', urls[1])) > 0:
		url_type = {
			'conupon_url' : urls[0],
			'item_url' : filter_item_url(urls[1])
		}
		return url_type
	elif len(re.findall(r'https?\:\/\/item\.m\.jd\.com\/product\/(\d+)\.html', urls[1])) > 0:
		url_type = {
			'conupon_url' : urls[0],
			'item_url' : filter_item_url(urls[1])
		}
		return url_type
	else:
		# 循环解析302跳转
		# tmp = jdcompoundspiderclass.analyticalurl.analytica_for_durl(urls[0])
		# if tmp != None:
		# 	# 如果解析发现是302跳转，使用解析后的内容
		# 	urls[0] = tmp
		tmp = jdcompoundspiderclass.analyticalurl.analytica_for_durl(urls[1])
		# print u'urls setp 1'
		# print tmp
		if tmp != None and tmp != 'https://www.jd.com/?d':
			# 如果解析发现是302跳转，使用解析后的内容
			urls[1] = tmp
		# print u'urls setp 2'
		# print urls
		if jdcompoundspiderclass.analyticalurl.analytica_durl(urls[0]) == 'is coupon' and jdcompoundspiderclass.analyticalurl.analytica_durl(urls[1]) == None:
			url_type = {
				'conupon_url' : urls[0],
				'item_url' : filter_item_url(urls[1])
			}
			return url_type
	# print url_type
	return url_type


@bot.register(Group, TEXT)
def print_group_msg(msg):
	# time.sleep(1)
	print msg.text

	# 设置错误提醒消息群
	wxpy_groups = bot.groups().search(u'summer_group_0001')
	# print wxpy_groups
	group = wxpy_groups[0]

	content = msg.text
	# print 'qq: ' + member.qq
	# 判断特殊标记，如果有，则不处理。
	tmp = re.findall(r'(\-\=\[ orz \]\=\-).+', content)
	if len(tmp) > 0:
		print u'有特殊标记，不处理'
		return
	tmp = re.findall(r'(\-\=\[ REDRUM \]\=\-).+', content)
	if len(tmp) > 0:
		print u'有特殊标记，不处理'
		return

	# 过滤消息
	content_tmp = filter_special_characters(content)

	# 提取文本中的URL
	urls = get_url_from_content(content_tmp)
	# print urls
	url_type = check_url_type(urls, content)
	if url_type != None:
		print u'conupon_url: ' + str(url_type['conupon_url'])
		print u'item_url: ' + str(url_type['item_url'])
		conupon_url = url_type['conupon_url']
		item_url = url_type['item_url']

		get_info_ify = jdcompoundspiderclass.get_info(item_url, conupon_url, '2')
		if get_info_ify == True:
			print u'上传成功'
		else:
			tmp = re.findall(r'(http)', content)
			if len(tmp) > 0:
				# 解析失败，发送消息
				group.send(u'-=[ REDRUM ]=- 转发时删除该行' + "\n" + content)
				time.sleep(1)
				group.send(get_info_ify)

	else:
		tmp = re.findall(r'(http)', content)
		if len(tmp) > 0:
			# print u'求抱大腿~~~~~'
			group.send(u'-=[ orz ]=- 转发时删除该行' + "\n" + content)

embed()
