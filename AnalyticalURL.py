# -*- coding: utf-8 -*-

# URL解析
# 用于解析京东的各种200、302跳转，得到真实的商品ID、劵地址

import config

import requests, requests.packages.urllib3
import re, os, time, sys
import logging, logging.handlers
import urlparse

requests.packages.urllib3.disable_warnings()
reload(sys)
sys.setdefaultencoding('utf-8')

class AnalyticalURL():

    def __init__(self):

        self.sess = requests.Session()
        self.cookies = {}
        self.headers = {
            'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
            'ContentType': 'text/html; charset=utf-8',
            'Accept-Encoding':'gzip, deflate, sdch',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'Connection' : 'keep-alive',
        }

    def set_sess(self, sess):
        self.sess = sess

    def set_cookies(self, cookies):
        self.cookies = cookies



    # 对外方法：获取真实的商品地址
    def get_real_item_url(self, url):
        # print url
        real_url = None
        analytica_type = self.check_url(url)

        if analytica_type == 'union-click.jd.com':
            # print u'item union-click.jd.com'
            return self.analytica_union_click(url)
        if analytica_type == 'item.jd.com':
            # print u'item item.jd.com'
            return self.analytica_item(url)
        if analytica_type == 'durl':
            # print u'item durl'
            return self.analytica_302(url)
        return real_url


    # 对外方法：获取真实的劵地址
    def get_real_coupon_url_new(self, url):
        real_url = None
        tmp = self.analytica_t_im(url)
        # print 'get_real_coupon_url_new self.analytica_t_im'
        # print tmp 
        # print '-----------------'
        if tmp != None:
            url = tmp

        real_url = self.get_key_and_roleid(url)
        return real_url


    # 对外方法：获取真实的劵地址
    def get_real_coupon_url(self, url):
        # return self.get_real_coupon_url_new(url)
        # print url
        # 首次尝试获取 key 和 roleid 如果有，则直接返回
        real_url = self.get_key_and_roleid(url)
        if real_url != None:
            return real_url

        real_url = None
        analytica_type = self.check_url(url)

        if analytica_type == 'durl':
            # print u'coupon ' + analytica_type
            tmp = self.analytica_302(url)
            # print u'过渡URL ' + str(tmp)
            if tmp == None:
                return real_url
            real_url = self.get_key_and_roleid(tmp)
        if analytica_type == 't.im':
            # print u'coupon ' + analytica_type
            tmp = self.analytica_t_im(url)
            # print u'过渡URL ' + str(tmp)
            if tmp == None:
                return real_url
            real_url = self.get_key_and_roleid(tmp)
        if analytica_type == 'jd.com_ilink':
            # print u'coupon ' + analytica_type
            # print u'过渡URL ' + str(url)
            real_url = self.get_key_and_roleid(url)
        if analytica_type == 'coupon':
            # print u'coupon ' + analytica_type
            # print u'过渡URL ' + str(url)
            real_url = self.get_key_and_roleid(url)
        return real_url




    # 判断URL是否需要解析，以什么方式来解析
    def check_url(self, url):
        # print u'check_url ------'
        analytica_type = None

        tmp = re.findall(r"[http|https]\:\/\/item\.jd\.com\/(\d+)\.html", url)
        # print len(tmp), tmp
        if len(tmp) > 0:
            return 'item.jd.com'

        tmp = re.findall(r"[http|https]\:\/\/item\.m\.jd\.com\/ware\/view\.action\?wareId\=(\d+)", url)
        # print len(tmp), tmp
        if len(tmp) > 0:
            return 'item.jd.com'

        tmp = re.findall(r"[http|https]\:\/\/item\.m\.jd\.com\/product\/(\d+)\.html", url)
        # print len(tmp), tmp
        if len(tmp) > 0:
            return 'item.jd.com'

        tmp = re.findall(r"[http|https]\:\/\/union\-click\.jd\.com\/jdc\?d\=(\w+)", url)
        # print len(tmp), tmp
        if len(tmp) > 0:
            return 'union-click.jd.com'

        tmp = re.findall(r"[http|https]\:\/\/t\.cn\/(\w+)", url)
        # print len(tmp), tmp
        if len(tmp) > 0:
            return 'durl'

        tmp = re.findall(r"https?\:\/\/[www\.]*dwz\.cn\/(\w+)", url)
        # print len(tmp), tmp
        if len(tmp) > 0:
            return 'durl'

        tmp = re.findall(r"https?\:\/\/suo\.im\/(\w+)", url)
        # print len(tmp), tmp
        if len(tmp) > 0:
            return 'durl'

        tmp = re.findall(r"https?\:\/\/sep9\.cn\/(\w+)", url)
        # print len(tmp), tmp
        if len(tmp) > 0:
            return 'durl'

        tmp = re.findall(r"https?\:\/\/jd\.cn\.hn\/(\w+)", url)
        # print len(tmp), tmp
        if len(tmp) > 0:
            return 'durl'

        tmp = re.findall(r"https?\:\/\/t\.im\/(\w+)", url)
        # print len(tmp), tmp
        if len(tmp) > 0:
            return 't.im'

        tmp = re.findall(r"https?\:\/\/coupon\.jd\.com\/ilink\/couponActiveFront\/front_index\.action\?key\=\w+\&roleId\=\d+", url)
        # print len(tmp), tmp
        if len(tmp) > 0:
            return 'jd.com_ilink'

        tmp = re.findall(r"https?\:\/\/coupon\.jd\.com\/ilink\/couponSendFront\/send_index\.action\?key\=\w+\&roleId\=\d+", url)
        # print len(tmp), tmp
        if len(tmp) > 0:
            return 'jd.com_ilink'

        tmp = re.findall(r"https?\:\/\/jd\.cn\.hn\/(\w+)", url)
        # print len(tmp), tmp
        if len(tmp) > 0:
            return 'durl'

        tmp = re.findall(r"https?\:\/\/u6\.gg\/(\w+)", url)
        # print len(tmp), tmp
        if len(tmp) > 0:
            return 'durl'

        tmp = re.findall(r"https?\:\/\/c7\.gg\/(\w+)", url)
        # print len(tmp), tmp
        if len(tmp) > 0:
            return 'durl'

        tmp = re.findall(r"https?\:\/\/tb0\.cn\/(\w+)", url)
        # print len(tmp), tmp
        if len(tmp) > 0:
            return 'durl'

        tmp = re.findall(r"https?\:\/\/coupon\.m\.jd\.com\/coupons\/show\.action\?key\=\w+\&roleId\=\d+", url)
        # print len(tmp), tmp
        if len(tmp) > 0:
            return 'coupon'

        return analytica_type



    # 解析 item 跳转
    def analytica_item(self, url):
        real_url = None
        tmp = re.findall(r"[http|https]\:\/\/item\.jd\.com\/(\d+)\.html", url)
        if len(tmp) > 0:
            real_url = 'https://item.jd.com/' + str(tmp[0]) + '.html'
        tmp = re.findall(r"[http|https]\:\/\/item\.m\.jd\.com\/ware\/view\.action\?wareId\=(\d+)", url)
        if len(tmp) > 0:
            real_url = 'https://item.jd.com/' + str(tmp[0]) + '.html'
        tmp = re.findall(r"[http|https]\:\/\/item\.m\.jd\.com\/product\/(\d+)\.html", url)
        if len(tmp) > 0:
            real_url = 'https://item.jd.com/' + str(tmp[0]) + '.html'

        return real_url



    # 解析 302 跳转
    def analytica_302(self, url):
        real_url = None
        res = self.sess.head(url)
        real_url = res.headers.get('location')
        # TODO 
        # 结果校验
        return real_url



    # 解析 t.im 跳转
    def analytica_t_im(self, url):
        real_url = None
        r = self.sess.get(
            url, 
            headers = self.headers,
            cookies = self.cookies
        )
        hrl = re.findall(r'\<a href\=\"(.+)\" class\=\"btn btn\-success\"\>', r.text)
        if len(hrl) > 0:
            real_url = hrl[0]
        else:
            # print u'get t.im hrl err'
            pass
        return real_url



    # 解析 JS 跳转，用于解析带跳转的商品地址。 
    #   eg: https://union-click.jd.com/jdc?d=X5riiL 
    #   转换为
    #   https://item.jd.com/11422307143.html
    def analytica_union_click(self, url):
        real_url = None
        r = self.sess.get(
            url, 
            headers = self.headers,
            cookies = self.cookies
        )
        hrl = re.findall(r"\; hrl=\'(.+)\' \;", r.text)
        if len(hrl) > 0:
            # print hrl
            hrl2 = self.analytica_302(hrl[0])
            skuid = re.findall(r"view\?sku\=(\d+)\&", hrl2)
            if len(skuid) > 0:
                real_url = 'https://item.jd.com/' + str(skuid[0]) + '.html'
                return real_url

            skuid = re.findall(r"https?\:\/\/re\.jd\.com\/cps\/item\/(\d+)\.html", hrl2)
            if len(skuid) > 0:
                real_url = 'https://item.jd.com/' + str(skuid[0]) + '.html'
                return real_url
            # print u'get hrl err'
            return real_url
        else:
            # print u'get hrl err'
            pass
        return real_url



    # 提取 key 和 roleid 并拼装领卷地址
    def get_key_and_roleid(self, url):
        couponsurl = None
        key_and_roleid = self.get_key_and_roleid_new(url)
        if key_and_roleid != None:
            # 拼装领卷地址
            couponsurl = 'http://coupon.m.jd.com/coupons/show.action?key=' + str(key_and_roleid['key']) + '&roleId=' + str(key_and_roleid['roleid']) + '&to=mall.jd.com/'
        return couponsurl



    # 提取 key 和 roleid
    # 不管URL是否是真正的领卷地址，都强行解析，然后自行拼装URL，避免一些带sid的URL来干扰采集。
    # eg: 
    #   https://item.jd.com/10803567517.html,http://coupon.m.jd.com/coupons/show.action?key=9837ad6ac8b14bd5a2c657c035547c5e&roleId=6301638&to=dazhiran.jd.com&sid=362bb980739c0487f28accd98bf695e6
    # 这种类型的URL会导致已经登录的脚本再次去登录
    def get_key_and_roleid_new(self, url):
        key_and_roleid = None
        # 解析出 key 和 roleId 的值
        # key
        try:
            key = re.findall(r"\?key ?\=(\w{32})\&?", url)
            if len(key) < 1:
                key = re.findall(r"\?keyid ?\=(\w{32})\&?", url)
            if len(key) < 1:
                key = re.findall(r"\?keyid ?\=(\w{32})\%20\&", url)
            if len(key) < 1:
                key = re.findall(r"\%3Fkey ?\%3D(\w{32})\%26", url)
            if len(key) < 1:
                return key_and_roleid
        except Exception, e:
            print u'get key err %s', e
            return key_and_roleid
        # roleId
        try:
            roleId = re.findall(r"\&roleId ?\=(\d+)\&?", url)
            if len(roleId) < 1:
                roleId = re.findall(r"\&roleid ?\=(\d+)\&?", url)
            if len(roleId) < 1:
                roleId = re.findall(r"\%26roleId ?\%3D(\d+)\%26", url)
            if len(roleId) < 1:
                roleId = re.findall(r"\&amp\;roleId ?\=(\d+)\&?", url)
            if len(roleId) < 1:
                return key_and_roleid
        except Exception, e:
            print u'get roleid err %s', e
            return key_and_roleid
        return  {
            'key': str(key[0]),
            'roleid': str(roleId[0])
        }


    # 混合解析、判断域名
    def analytica_durl(self, url):
        tmp = self.analytica_item(url)
        if tmp != None:
            tmp = self.get_key_and_roleid_new(tmp)
            if tmp != None:
                return 'is coupon'

        tmp = self.analytica_302(url)
        if tmp != None:
            tmp = self.get_key_and_roleid_new(tmp)
            if tmp != None:
                return 'is coupon'

        tmp = self.analytica_t_im(url)
        if tmp != None:
            tmp = self.get_key_and_roleid_new(tmp)
            if tmp != None:
                return 'is coupon'

        tmp = self.analytica_union_click(url)
        if tmp != None:
            tmp = self.get_key_and_roleid_new(tmp)
            if tmp != None:
                return 'is coupon'

        return None



    # 混合解析、判断域名
    def analytica_for_durl(self, url):
        ify = True
        url_tmp = url
        url_tmp_old = url
        # 循环解析302跳转
        while ify:
            url_tmp = self.analytica_302(url_tmp)
            if url_tmp == None:
                url_tmp = url_tmp_old
                break
            else:
                url_tmp_old = url_tmp
        # print url_tmp
        return url_tmp


