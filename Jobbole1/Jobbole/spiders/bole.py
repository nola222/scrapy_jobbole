# -*- coding: utf-8 -*-
import scrapy
from scrapy.http.request import  Request
from Jobbole.items import JobboleItem
# 使用CrawlSpider 继承于scrapy.Spider
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
import re
# 设置logging
import logging

logger = logging.getLogger('nola222222222')

class BoleSpider(CrawlSpider):
	name = 'bole'
	allowed_domains = ['jobbole.com']
	start_urls = ['http://python.jobbole.com/all-posts/page/0/']
	# http: // python.jobbole.com / all - posts / page / 2 /

	'''
	# Rule主要参数 link_extractor(为LinkExtractor()类的实例),
	  callback注意不能为parse CrawlSpider会调用parse 免得被覆盖,
	  follow根据该rule提取的response是否需要跟进
	# 为LinkExtractor主要参数 allow 允许的链接(正则)，deny(不允许的)
	'''
	# 下面元祖 最后加个逗号

	rules = (
		Rule(LinkExtractor(allow=r'page/\d+/'),callback='parse_item',follow=True),
	)

	# 写规则后 不需要自定义请求
	# # 自定义请求
	# def start_requests(self):
	#
	# 	url = 'http://python.jobbole.com/all-posts/page/0/'
	# 	yield Request(url=url,callback=self.parse_item)

	def parse_item(self, response):
		logger.info('parse function...........11111')
		# 出现xe/ decode解码一下
		# print(response.body.decode('utf-8'))
		items = response.xpath('//div[@class="post floated-thumb"]/div[@class="post-thumb"]/a')
		# print(len(items)) 20
		for item in items:
			# 文章链接 extract()返回的是list extract_first()返回的是一个值 str类型
			art_url = item.xpath('./@href').extract_first()
			# 文章标题
			art_title = item.xpath('./@title').extract_first()
			# 文章图片链接
			art_img_url = item.xpath('./img/@src').extract_first()
			# print(art_list,art_title,art_img_url)

			# 请求文章链接
			yield Request(url=art_url,callback=self.parse_content,meta={'art_url':art_url,'art_title':art_title,'art_img_url':art_img_url})

		# 实现翻页 在解析页面的函数中写代码  点击下一页
		# 获得下一页的链接
		# next_page = response.xpath('//div[@class="navigation margin-20"]/a[@class="next page-numbers"]/@href').extract_first()
		# print(next_page)
		# print('正在翻页----第%s页----' % (next_page[-2:-1]))
		# if not next_page:
		# 	print('翻页完毕！！！')
		# yield Request(url=next_page, callback=self.parse)

	def parse_content(self,response):
		# items = ItemLoader(item=JobboleItem(),response=response)
		# # 匹配创建时间
		# items.add_xpath('create_time','//p[@class="entry-meta-hide-on-mobile"]/text()')
		# print(create_time)
		# return items.load_item()

		# 实例化items  给items字段赋值
		items = JobboleItem()
		# 文章创建时间 -- 这个函数会传到上面的for循环中 所以这里都是取第一个
		create_time = response.xpath('//div[@class="entry-meta"]/p/text()').extract_first().strip()
		create_time = create_time.replace(' ·','').replace('/','-')
		items['create_time'] = create_time
		# 内容 -- 只抓取了p标签内容
		art_content = response.xpath('//div[@class="entry"]/p/text()').extract()
		items['art_content'] = art_content
		# 接收传下来的数据
		art_url = response.meta['art_url']
		items['art_url'] = art_url
		art_title = response.meta['art_title']
		items['art_title'] = art_title
		art_img_url = response.meta['art_img_url']
		items['art_img_url'] = art_img_url
		# 拼接数据
		art_list = {
			'art_url' : art_url,
			'art_title':art_title,
			'art_img_url':art_img_url,
			'create_time':create_time,
			'art_content':art_content
		}
		# 将数据返回给piplines.py
		# print(art_list)
		return items