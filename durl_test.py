# -*- coding: utf-8 -*-

# 短链接测试

import json, os, time, sys, re
import JdItemsPage
import requests
import AnalyticalURL
import ExistingCommodity
import MjdLogin

from lxml import etree

analyticalurl = AnalyticalURL.AnalyticalURL()
jditemspage = JdItemsPage.JdItemsPage()
existingcommodity = ExistingCommodity.ExistingCommodity()
mjdlogin = MjdLogin.MjdLogin()

mjdlogin.check_login()

def find_all_url(sentence, show_urls = None, delete_urls = None):
    #r = re.compile(r'(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))')
    r = re.compile(r'((?:http|https)://[\w\-\.,@?^=%&:\/~\+#]+)')
    url_list = r.findall(sentence)
    if show_urls == 1:
        print "find", str(len(url_list)), "URLs"
        for i in url_list:
            print i

    if delete_urls == 1:
        for j in url_list:
            # sentence = sentence.replace(j[0], '<URL>')
            sentence = sentence.replace(j[0], '')
        return sentence
    return 1

def revertShortLink(url):
    res = requests.head(url)
    return res.headers.get('location')

	
def filter_item_url(url):
	# 删除结尾 - 字符
	tmp = url.strip().lstrip().rstrip(',').rstrip('-')
	# print tmp
	# 删除结尾 SKU:xxxx
	tmp2 = re.findall(r'((?i)SKU: ?\d+)$', tmp)
	if len(tmp2) > 0:
		tmp = tmp.replace(tmp2[0], '')
		# print tmp
	# 删除结尾 SKUID:xxxx
	tmp2 = re.findall(r'((?i)SKU： ?\d+)$', tmp)
	if len(tmp2) > 0:
		tmp = tmp.replace(tmp2[0], '')
		# print tmp
	return tmp


def get_key_and_roleid_new(url):
    key_and_roleid = None
    # 解析出 key 和 roleId 的值
    # key
    try:
        key = re.findall(r"\?key\=(\w{32})\&?", url)
        if len(key) < 1:
            key = re.findall(r"\?keyid\=(\w{32})\&?", url)
        if len(key) < 1:
            key = re.findall(r"\?keyid\=(\w{32})\%20\&", url)
        if len(key) < 1:
            key = re.findall(r"\%3Fkey\%3D(\w{32})\%26", url)
        if len(key) < 1:
            return key_and_roleid
    except Exception, e:
        print u'get key err %s', e
        return key_and_roleid
    # roleId
    try:
        roleId = re.findall(r"\&roleId\=(\d+)\&?", url)
        if len(roleId) < 1:
            roleId = re.findall(r"\&roleid\=(\d+)\&?", url)
        if len(roleId) < 1:
            roleId = re.findall(r"\%26roleId\%3D(\d+)\%26", url)
        if len(roleId) < 1:
            roleId = re.findall(r"\&amp\;roleId\=(\d+)\&?", url)
        if len(roleId) < 1:
            return key_and_roleid
    except Exception, e:
        print u'get roleid err %s', e
        return key_and_roleid
    return  {
        'key': str(key[0]),
        'roleid': str(roleId[0])
    }


rexp = '((ht|f)tps?):\/\/[\w\-]+(\.[\w\-]+)+([\w\-\.,@?^=%&:\/~\+#]*[\w\-\@?^=%&\/~\+#])?'
rexp2 = r"https?:\/\/[\w-.%#?\/]+"

urls = [
	# 'http://jd.cn.hn/fVS',
	# 'https://0x5.me/vteJ',
	# '领卷：http://coupon.m.jd.com/coupons/show.action?key=b4ef6fe943c94d06b8aaeb7ad347d63b&roleId=6373489&to=mall.jd.com/ 【打飞机克里斯多夫',
	# '领券：https://coupon.jd.com/ilink/couponSendFront/send_index.action?key=523cd7f462bb4e7f83c7a4f03d3701a6&roleId=6459837&to=mall.jd.com/index-632626.html——下单：https://item.jd.com/11193452292.html',
	# '霸王 黑芝麻黑亮洗发露套装 黑芝麻洗发露1L+乌发固发洗发液400ml————————————原价：￥78.00。优惠价：￥39.00。————————————购买链接：https://union-click.jd.com/jdc?d=FmjXGS【京东配送】',
	# '【夏天流汗也不怕】立体流畅防水眼线笔2ml————————————原价：￥37.90。专享价：￥9.90。（券后）领券：http://jd.cn.hn/gaR————————————购买链接：https://union-click.jd.com/jdc?d=TykIIQ【京东配送】',
	# 'https://item.jd.com/12032559216.html-----------------------------------------',
	# '买链接：https://union-click.jd.com/jdc?d=cGzcF1SKU:12189862224     ',
	# '买链接：https://union-click.jd.com/jdc?d=cGzcF1SKU:12189862224',
	# '买链接：https://union-click.jd.com/jdc?d=cGzcF1sku:12189862224',
	# '买链接：https://union-click.jd.com/jdc?d=cGzcF1sKu:12189862224',
	# '买链接：https://union-click.jd.com/jdc?d=cGzcF1sKu: 12189862224',
	# '买链接：https://union-click.jd.com/jdc?d=cGzcF1sKu：12189862224',
	# '买链接：https://union-click.jd.com/jdc?d=cGzcF1sKu： 12189862224',
	# 'http://c7.gg/pJr',
	# 'http://u6.gg/pJr',
	# 'http://jd.cn.hn/mqB',
	# 'http://t.cn/RSKwTEF',
	# 'http://t.cn/RSK5tos',
	# 'http://t.cn/RSK5tos',
    # 'http://coupon.m.jd.com/coupons/show.action?key=e1767ab8d210443991e388957cd9ebce&roleId=6541123',
    # 'https://0x9.me/Dzoyc',
    # 'http://dwz.cn/66scYt',
    # 'http://t.cn/RSR7W5d',
    # 'http://tb0.cn/RmX753',
    # 'https://s.tuikemao.cn/s/g2jfqa8h/11100422162',
    'http://dwz.cn/6azVrE',
]



for url in urls:
	# print analyticalurl.get_real_coupon_url(url)
	print revertShortLink(url)
	# print get_key_and_roleid_new(url)
	# m = re.match(rexp, url)
	# if m:
	# 	print m.group(0)
	# m2 = re.findall(rexp2, url)
	#tmp = re.sub(r"[^\x00-\xff]+", ' ', url)
	#print tmp
	# find_all_url(url, show_urls=1)
	# print filter_item_url(url)
