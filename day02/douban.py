import json
import requests
import re
from lxml import etree


# 取页面HTML
def get_one_page(offset):
	url = "https://www.douban.com/group/explore?start=%d" % offset
	headers = {
		"User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)"
	}
	response = requests.get(url, headers=headers)
	if response.status_code == 200:
		text = response.content.decode('utf-8')
		return text
	return None


# 解析页面
def parse_with_xpath(html):
	etree_html = etree.HTML(html)
	# print(etree_html)

	# 匹配所有节点 //*
	# result = etree_html.xpath('//*')
	# print(result)
	# print(len(result))

	# 匹配所有子节点 //a     文本获取：text()
	# result = etree_html.xpath('//a/text()')
	# print(result)

	# 查找元素子节点 /
	# result = etree_html.xpath('//div/p/text()')
	# print(result)

	# 查找元素所有子孙节点 //
	title_result = etree_html.xpath('//div[@class="channel-item"]//h3/a/text()')
	# print(title_result)

	# 父节点 ..
	# name_result = etree_html.xpath('//span[@class="pubtime"]/../span/a/text()')
	# print(result)

	# 匹配地址
	url_result = etree_html.xpath('//div[@class="source"]//span[@class="from"]/a/@href')

	# 属性匹配 [@class="xxx"]
	# 文本匹配 text() 获取所有文本//text()
	# result = etree_html.xpath('//div[@class="article"]//text()')
	# print(result)

	# 属性获取 @href
	# result = etree_html.xpath('//div[@class="bd"]/h3/a/@href')
	# print(result)

	# 属性多值匹配 contains(@class 'xx')
	# result = etree_html.xpath('//div[contains(@class, "grid-16-8")]//div[@class="likes"]/text()[1]')
	# print(result)

	# 多属性匹配 or, and, mod, //book | //cd, + - * div = != < > <= >=
	# result = etree_html.xpath('//span[@class="pubtime" and contains(text(), "09-07")]/text()')
	# print(result)

	# 按序选择 [1] [last()] [poistion() < 3] [last() -2]
	# 节点轴
	# //li/ancestor::*  所有祖先节点
	# //li/ancestor::div div这个祖先节点
	# //li/attribute::* attribute轴，获取li节点所有属性值
	# //li/child::a[@href="link1.html"]  child轴，获取直接子节点
	# //li/descendant::span 获取所有span类型的子孙节点
	# //li/following::* 选取文档中当前节点的结束标记之后的所有节点
	# //li/following-sibling::*     选取当前节点之后的所用同级节点

	# result = etree_html.xpath('//img/attribute::*')
	# print(result)

	# result = etree_html.xpath('//div[contains(@class, "channel-group-rec")]//div[@class="title"]/following::*[1]/text()')
	# print(result)
	message = []
	for i in range(len(title_result)):
		information = {}
		# information['name'] = name_result[i].strip()
		information['title'] = title_result[i].strip()
		information['url'] = url_result[i].strip()
		message.append(information)
	return message


def get_all_page():
	items = {}
	for i in range(298):
		offset = i * 30
		html = get_one_page(offset)
		message = parse_with_xpath(html)
		page_name = 'page%d' % (i + 1)
		items[page_name] = message
		print(page_name)
	str = json.dumps(items, ensure_ascii=False)
	with open('./douban.json', 'w', encoding='utf-8')as f:
		f.write(str)


def main():
	# html = get_one_page()
	# # print(html)
	# parse_with_xpath(html)
	get_all_page()


if __name__ == '__main__':
	main()