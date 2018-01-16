import scrapy
import json
import os
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from chainxy.items import ChainItem
from lxml import html
import random
import usaddress
import pdb

class ebayzoroSpider(scrapy.Spider):
	name = 'ebay-zoro'
	domain = 'http://stores.ebay.com'
	count = 0
	ind = 0

	def start_requests(self):
		self.proxy_list = [	
							'https://165.138.77.64:8080',
							'https://198.11.137.71:80',
							'https://35.186.163.245:3128',
							'https://35.186.160.98:80',
							'https://65.28.254.186:8080',
							'https://206.51.35.177:53281',
							'https://35.160.75.160:80',
							'https://54.219.152.193:80',
							'https://104.131.92.77:80',
							'https://198.23.74.170:81',
							'https://63.110.242.67:3128',
							'https://149.39.18.152:80',
							'https://173.212.49.74:8080',
							'https://12.199.82.226:8080',
							'https://172.81.78.65:8080',
							'https://209.163.160.253:8080',
							'https://104.245.69.17:3128',
							'https://69.10.52.33:8080',
							'https://76.79.39.162:8080',
							'https://50.254.42.84:8080',
							'https://104.236.156.92:8080',
							'https://47.91.139.85:8123',
							'https://192.129.241.42:9001',
							'https://64.183.94.45:8080',
							'https://192.129.165.189:9001',
							'https://68.185.106.196:80',
							'https://216.195.96.130:8080',
							'https://66.162.122.25:8080',
							'https://34.210.9.216:80',
							'https://45.79.99.200:80',
							'https://96.66.42.149:8080',
							'https://192.129.214.20:9001',
							'https://54.175.72.127:80',
							'https://107.170.61.29:8080',
							'https://205.196.181.10:8080',
							'https://31.220.58.65:8080',
							'https://45.33.56.186:3128',
							'https://54.173.129.116:6666',
							'https://13.66.60.134:3128',
							'https://162.243.18.46:3128',
							'https://170.24.131.171:3128',
							'https://199.195.253.124:3128',
							'https://170.185.171.14:8080',
							'https://205.202.35.228:8080',
							'https://168.128.29.75:80',
							'https://216.100.88.229:8080',
							'https://165.138.77.67:8080',
							'https://12.27.33.3:8080',
							'https://47.52.33.216:3128',
							'https://104.199.183.252:3128',
							'https://205.196.181.12:8080',
							'https://104.131.19.130:8080',
							'https://47.91.150.215:3128',
							'https://47.52.3.230:443',
							'https://97.78.0.26:3128',
							'https://50.234.99.162:3128',
							'https://216.1.75.135:80',
							'https://216.1.75.139:80',
							'https://47.89.208.49:3128',
							'https://66.115.236.15:8080',
							'https://181.215.115.114:8800',
							'https://104.224.168.178:8888',
							'https://216.1.75.136:80',
							'https://162.213.3.155:4444',
							'https://54.70.247.41:8080',
							'https://142.54.164.106:3721',
							'https://74.83.246.105:8081',
							'https://208.108.130.128:80	',
							'https://192.129.205.200:9001',
							'https://216.1.75.152:80',
							'https://198.23.143.27:8080',
							'https://216.1.75.134:80',
							'https://107.183.253.165:8118',
							'https://23.105.86.50:8118',
			
						  ]

		init_url = 'http://stores.ebay.com/Zoro-Tools/Gloves-Safety-Apparel-/_i.html?_fsub=4143466014&_sid=1113381714&_trksid=p4634.m322'
		header = {
			"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
			"Accept-Encoding":"gzip, deflate, sdch"
		}
		self.count += 1
		if self.count% 8000 == 0:
			self.ind += 1
		yield scrapy.Request(url=init_url, headers=header, method='get', callback=self.parse_category, meta={'proxy':self.proxy_list[self.ind]})

	def parse_category(self, response):
		data = response.body.split('CascadeMenu({"modelList":')[1].split('}));')[0].strip()
		category_list = json.loads(data)
		for category in category_list:
			for sub_category in category['children']:
				self.count += 1
				if self.count% 8000 == 0:
					self.ind += 1
				link = self.domain + self.validate(sub_category['main']['url'])
				yield scrapy.Request(url=link, callback=self.parse_product, meta={'proxy':self.proxy_list[self.ind]})		

	def parse_product(self, response):
		product_list = response.xpath('//a[@class="v4lnk"]/@href').extract()
		for product in product_list:
			self.count += 1
			if self.count% 8000 == 0:
				self.ind += 1
			link = 'http://vi.vipr.ebaydesc.com/ws/eBayISAPI.dll?ViewItemDescV4&item=' + product.split('/')[-1].strip().split('?')[0]
			yield scrapy.Request(url=link, callback=self.parse_detail, meta={'proxy':self.proxy_list[self.ind]})

		try:
			pagenation = response.xpath('//a[@class="pg"]')
			pagenation = pagenation[len(pagenation)-1].xpath('./@href').extract_first()
			if pagenation:
				pagenation = self.domain + pagenation
				self.count += 1
				if self.count% 8000 == 0:
					self.ind += 1
				yield scrapy.Request(url=pagenation, callback=self.parse_product, meta={'proxy':self.proxy_list[self.ind]})
		except:
			pass
	
		# self.count += 1
		# try:
		# 	product_list = response.xpath('//table[@class="FbOuterYukon"]//tr[@class="bot"]')
		# 	# pdb.set_trace()
		# 	for product in product_list:
		# 		code = self.eliminate_space(product.xpath('.//text()').extract())
		# 		key = ''
		# 		for co in code:
		# 			if '(#' in co:
		# 				key = co.split('(#')[1].strip().split(')')[0]
		# 				url = 'http://vi.vipr.ebaydesc.com/ws/eBayISAPI.dll?ViewItemDescV4&item=' + key
		# 		# url = 'http://vi.vipr.ebaydesc.com/ws/eBayISAPI.dll?ViewItemDescV4&item=' + product.split('/')[-1].strip().split('?')[0]
			
		# 				yield scrapy.Request(url=url, callback=self.parse_detail, meta={'proxy':response.meta['proxy']})
		# 		# yield scrapy.Request(url=product, callback=self.parse_detail)
		# # 	# try:
		# # 	# 	if self.count % 200 == 0:
		# # 	# 		self.ind += 1
		# # 	# 	pagenation = response.xpath('//a[@class="gspr next"]/@href').extract_first()
		# # 	# 	if pagenation:
		# # 	# 		yield scrapy.Request(url=pagenation, callback=self.parse_product, meta={'proxy':self.proxy_list[self.ind]})
		# # 	# except:
		# # 	# 	pass
		# except:
		# 	pdb.set_trace()
	
	def parse_page(self, response):
		try:
			self.count += 1
			print('~~~~~~~~~~~~~~~', self.count)
			url = 'http://vi.vipr.ebaydesc.com/ws/eBayISAPI.dll?ViewItemDescV4&item=' + response.url.split('/')[-1].strip().split('?')[0]
			s_temp = ''
			spec_list = response.xpath('//div[@class="section"]//table//td')
			cnt = 1
			for spec in spec_list[4:]:
				temp = self.eliminate_space(spec.xpath('.//text()').extract())
				mid = ''
				for te in temp:
					mid += te + ' '
				if cnt % 2 == 0:
					s_temp += self.validate(mid) + ', '
				else :
					s_temp += self.validate(mid) + ' '
				cnt += 1
			yield scrapy.Request(url=url, callback=self.parse_detail, meta={'specifics':s_temp, 'proxy':random.choice(self.proxy_list)})
		except:
			pass

	def parse_detail(self, response):
		try:
			item = ChainItem()
			item['name'] = self.validate(response.xpath('//div[@class="container"]//h1/text()').extract_first())
			temp = self.validate(response.xpath('//div[@class="container"]//p[1]/text()').extract_first()).split(':')
			sku = ''
			for s in temp[1].split(',')[:-1]:
				sku = s + ', '
			item['sku'] = self.validate(sku[:-2])
			item['mpn'] = self.validate(temp[2])
			item['selling_price'] = self.validate(response.xpath('//div[@class="container"]//h3[1]/text()').extract_first()).split(':')[1].strip()
			# item['specifics'] = response.meta['specifics']
			item['description'] = self.validate(response.xpath('//div[@class="container"]//p[2]/text()').extract_first())
			item['image_link'] = self.validate(response.xpath('//div[@class="main-image"]//img//@src').extract_first())
			yield item
		except:
			pass

	def validate(self, item):
		try:
			return item.strip().replace('  ', '').replace('\r', '').replace('\n','')
		except:
			return ''

	def eliminate_space(self, items):
		tmp = []
		for item in items:
			if self.validate(item) != '':
				tmp.append(self.validate(item))
		return tmp
