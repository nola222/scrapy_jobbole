# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import json
from scrapy.conf import settings
# 写入mongodb
# 对抓取的数据进行后续处理，比如入库，去重等
# 如果改动pipline，要在settings中设置启动
class JobbolePipeline(object):
	# 下面连接数据库代码也可以写在process_item方法中，但是写在__init__中只需要连接一次
	def __init__(self):
		# self.client = pymongo.MongoClient('60.205.211.210',27017)
		# self.db = self.client['test']
		# self.collection = self.db['bole_online']
		# 定义mongodb配置 -- 标准写法
		self.client = pymongo.MongoClient(host=settings['MONGODB_HOST'],port=settings['MONGODB_PORT'])
		self.db = self.client[settings['MONGODB_DB']]
		self.collection = self.db[settings['MONGODB_COLLECTION']]



	# 这个形参item是接收scrapy脚本传过来的items，这个方法会将items自动拆分为键值对来进行写入数据库等后续操作
	def process_item(self, item, spider):
		print(item)
		# 注意写入mongo时，要dict()强转一下，否则会报TypeError
		self.collection.insert(dict(item))
		return item # 是为了写多条数据时将实体传给下一个

# 写入json文件 命令：scrapy crawl spider_name -o filename.json   -o output输出
class JsonPipeline(object):
	# 普通方式 -- 需要close文件
	# def __init__(self):
	# 	# 不指定路径 在项目同级目录下创建json文件 -- 内容比较规整
	# 	self.f = open('bolele.json','w',encoding='utf-8')
	#
	# def process_item(self,item,spider):
	# 	# 把dict转为json串
	# 	data = json.dumps(dict(item),ensure_ascii=False) + '\n'
	# 	self.f.write(data)
	# 	return item
	#
	# def close_spider(self):
	# 	self.f.close()

	# 安全方式open，不需要自己调用close
	def process_item(self,item,spider):
		with open('bbole.json','a+',encoding='utf-8') as f:
			# 把dict转为json串
			data = json.dumps(dict(item),ensure_ascii=False) + '\n'
			f.write(data)
		return item