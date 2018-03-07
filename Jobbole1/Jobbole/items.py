# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JobboleItem(scrapy.Item):
	# define the fields for your item here like:
	# name = scrapy.Field()
	art_url = scrapy.Field()
	art_title = scrapy.Field()
	art_img_url= scrapy.Field()
	create_time = scrapy.Field()
	art_content = scrapy.Field()

