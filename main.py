#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import getopt
import time
import os
import re
import urllib.request

def usage():
	print('Use "-d" set backup interval time.')
	print('Use "-u" set backup url.')
	print('Use "-o" set backup save path.')

def main():
	'''
	Back up for url.
	Default url: http://m.sohu.com
	File store in: /tmp/backup
	Interval back-up time: 60s
	'''
	cycle = 60
	url   = 'http://m.sohu.com'
	dirc  = '/tmp/backup'
	
	#Get shell arguments.
	try:
		opts, args = getopt.getopt(sys.argv[1:], "d:u:o:")
	except getopt.GetoptError as err:
		print(str(err))
		usage()
		sys.exit(2)
	for op, value in opts:
		if op == '-d':
			cycle = value
		elif op == '-u':
			url = value
		elif op == '-o':
			dirc = value


	if not os.path.isdir(dirc):
		os.makedirs(dirc)
	#Back up for the url
	while True:
		time_rule = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
		file_dirc = dirc + '/' + time_rule + '/'
		js_dirc     = file_dirc + 'js/'
		css_dirc    = file_dirc + 'css/'
		images_dirc = file_dirc + 'images/'
		os.makedirs(file_dirc)
		os.makedirs(js_dirc)
		os.makedirs(css_dirc)
		os.makedirs(images_dirc)
		print(time_rule)
		
		#Get html
		header = ('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86-64; rv:30.0) Gecko/20100101 Firefox/30.0')
		opener = urllib.request.build_opener()
		opener.addheaders = [header]
		page = opener.open(url).read()

		#Get js,css,images
		js_path = re.compile(b'src="(.*?)\.js"')
		css_path = re.compile(b'href="(.*?)\.css"')
		images_path = re.compile(b'src="(.*?)(\.gif|\.jpg|\.png)"')
		js_list = js_path.findall(page)
		css_list = css_path.findall(page)
		images_list = images_path.findall(page)
		images_list = list(set(images_list))

		#Deal with js
		for url_js in js_list:
			url_js += b'.js'
			js_name = url_js.split(b'/')[-1]
			js_cont = opener.open(url_js.decode('ASCII')).read()
			with open(js_dirc + js_name.decode('ASCII'), 'wb') as file_js:
				file_js.write(js_cont)
			page = re.sub(url_js, b'./js/'+js_name, page)

		#Deal with css
		for url_css in css_list:
			url_css += b'.css'
			css_name = url_css.split(b'/')[-1]
			css_cont = opener.open(url_css.decode('ASCII')).read()
			with open(css_dirc + css_name.decode('ASCII'), 'wb') as file_css:
				file_css.write(css_cont)
			page = re.sub(url_css, b'./css/'+css_name, page)

		#Deal with images
		for url_images in images_list:
			url_im = url_images[0] + url_images[1]
			im_name = url_im.split(b'/')[-1]
			im_cont = opener.open(url_im.decode('ASCII')).read()
			with open(images_dirc + im_name.decode('ASCII'), 'wb') as file_im:
				file_im.write(im_cont)
			page, count = re.subn(url_im, b'./images/'+im_name, page)

		with open(file_dirc+'index.html', 'wb') as file_html:
			file_html.write(page)

		time.sleep(60)


if __name__ == '__main__':
	main()
