#!/usr/bin/env python
# -*- coding: utf-8 -*-

from wsgiref.simple_server import make_server
import json
import AnalyticalURL

analyticalurl = AnalyticalURL.AnalyticalURL()

def application(environ, start_response):
	try:
		request_body_size = int(environ.get('CONTENT_LENGTH', 0))
	except (ValueError):
		request_body_size = 0
		return ''

	request_body = environ['wsgi.input'].read(request_body_size)
	json_data = json.loads(request_body)
	# print json_data
	data = {}
	if json_data.has_key('couponUrl'):
		print json_data['couponUrl']
		tmp = analyticalurl.get_real_coupon_url(json_data['couponUrl'])
		if tmp != None:
			data['couponUrl'] = tmp
		else:
			data['couponUrl'] = ''
	if json_data.has_key('itemUrl'):
		print json_data['itemUrl']
		tmp = analyticalurl.get_real_item_url(json_data['itemUrl'])
		if tmp != None:
			data['itemUrl'] = tmp
		else:
			data['itemUrl'] = ''
	if json_data.has_key('skuid'):
		print json_data['skuid']


	response_str = {
		"code" : "200",
		"msg" : "ok",
		"data" : data
	}


	start_response('200 OK',[('Content-Type','text/html')])
	return json.dumps(response_str)

httpd = make_server('localhost', 38001, application)
httpd.serve_forever()
