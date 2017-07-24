# -*- coding: utf-8 -*-
# 强制登录

import config

import re, os, time, sys
import requests
import urllib2
from pprint import pprint
import csv

import JdLogin 
import MjdLogin 

reload(sys)
sys.setdefaultencoding('utf-8')

# get function name
FuncName = lambda n=0: sys._getframe(n + 1).f_code.co_name
# 改变目录
os.chdir(sys.path[0])

jdlogin = JdLogin.JdLogin()
mjdlogin = MjdLogin.MjdLogin()

# 必要的登录
print u'京东联盟登录 ============================'
print jdlogin.login_by_QR()
# print jdlogin.login_by_webdrive()

print u'移动京东登录 ============================'
print mjdlogin.login_by_webdrive()



