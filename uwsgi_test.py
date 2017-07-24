# -*- coding: utf-8 -*-

# HTTP 交互，用于 URL 解析
import logging, logging.handlers
import sys,json
import cgi

logger = logging.getLogger('uwsgi')
logger.setLevel(logging.INFO)
rh=logging.handlers.TimedRotatingFileHandler('log/uwsgi.log','D')
fm=logging.Formatter("%(asctime)s  %(levelname)s - %(message)s","%Y-%m-%d %H:%M:%S")
rh.setFormatter(fm)
logger.addHandler(rh)

def read_obj(env): 
    if 'wsgi.input' in env: 
        return env['wsgi.input'] 
    else: 
        return sys.stdin

#获取HTTP POST数据
def get_http_post_data(env):
     content_length = int(env['CONTENT_LENGTH'])
     buf = read_obj(env).read(content_length)  #buf就是post的参数，当然还是个字符串
     return buf

#获取HTTP GET数据
def get_http_get_data(env):
     buf = env['QUERY_STRING']
     return buf
    

def application(environ, start_response):
	start_response('200 OK',[('Content-Type','text/html')])
	infolog=logger.info

	http_post_data = get_http_post_data(environ)
	http_get_data = get_http_get_data(environ)
	infolog('http_post_data : %s', http_post_data)
	infolog('http_get_data : %s', http_get_data)

	# d = cgi.FieldStorage(environ=environ, fp=environ['wsgi.input'], keep_blank_values=True)
	# url = d.getvalue("url")
	# skuid = d.getvalue("skuid")
	# infolog('skuid : %s', skuid)
	# infolog('url : %s', url)



	#返回格式化数据，json很好用:-)
	reply_json = {'code':0,'msg':'this is a demo return str'}
	return json.dumps(reply_json)
