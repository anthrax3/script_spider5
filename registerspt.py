# -*- coding:utf-8 -*-
import cookielib
import urllib
import urllib2
import string
import pytesseract
from get_image import *
REGISTER_URL = 'http://example.webscraping.com/user/register'

def parse_form(html):
	'''
	使用lxml来抓取登陆的HTML来获取_formkey等属性
	get the dic:
	data = {'name':'value',...}
	'''
	tree = lxml.html.fromstring(html)
	data = {}
	for e in tree.cssselect('form input'):
		if e.get('name'):
			data[e.get('name')] = e.get('value')
	return data

def register(first_name, last_name, email, password):
	'''
	注册脚本的完整代码
	'''
	cj = cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	html = opener.open(REGISTER_URL).read()
	form = parse_form(html)
	form['first_name'] = first_name
	form['last_name'] = last_name
	form['email'] = email
	form['password'] = form['password_two'] = password
	captcha = get_str(html)
	form['recaptcha_response_field'] = captcha
	encoded_data = urllib.urlencode(form)
	request = urllib2.Request(REGISTER_URL, encoded_data)
	response = opener.open(request)

	# 验证是否注册成功
	success = '/user/register' not in response.geturl()
	return success

if __name__ == '__main__':
	first_name = 'yuan'
	last_name = 'gong'
	email = 'gongyuan1100@163.com'
	password = 'gongyuan110'
	result = register(first_name,last_name,email,password)
	print result