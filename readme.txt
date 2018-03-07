1.仓库scrapy_practice项目Jobbole使用的是scrapy.Spider
本次还是抓伯乐在线，使用的是scrapy.Spider.CrawlSpider

2.项目依赖参考requirements.txt

3.使用遵循Rule规则进行翻页

4.实现代码保存响应信息到文件

5.命令保击中格式文件：
	json：
		scrapy crawl spider_name -o xxx.json
	jsonlines:
		scrapy crawl spider_name -o xxx.jsonlines
	xml:
		scrapy crawl spider_name -o xxx.xml

	# -o --- output 输出到