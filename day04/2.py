import time

import pymysql
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import quote
from lxml import etree

chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
browser = webdriver.Chrome(chrome_options=chrome_options)


browser.set_window_size(1400, 700)
wait = WebDriverWait(browser, 5)
KEYWORD = '跑步鞋'


def get_page(page):
	if page == 1:
		url = 'https://search.jd.com/Search?keyword=%s&enc=utf-8' % quote(KEYWORD)
		browser.get(url)
		time.sleep(3)
	if page > 1:
		for i in range(8):
			str_js = 'var step=step = document.body.scrollHeight/8;window.scrollTo(0,step * %d)' %(i+1)
			browser.execute_script(str_js)
			time.sleep(1)
		input = wait.until(
			EC.presence_of_element_located((By.CSS_SELECTOR, '#J_bottomPage input.input-txt')))
		input.clear()
		input.send_keys(page)

		submit = wait.until(
			EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_bottomPage a.btn.btn-default')))
		submit.click()
	page_source = browser.page_source
	return page_source


def parse_page(page_source):
	etree_html = etree.HTML(page_source)
	print(type(etree_html))
	products = etree_html.xpath('///div[@id="J_goodsList"]/ul/li[contains(@class,"gl-item")]')
	print(len(products))
	print('*********************************************************************88')

	for product in products:
		item = {}
		product_img = product.xpath('.//div[@class="p-img"]/a/@href')
		item['img'] = product_img[0].strip() if product_img else ''
		product_price = product.xpath('.//div[contains(@class, "p-price")]/strong/i/text()')
		item['price'] = product_price[0].strip() if product_price else ''
		product_name = product.xpath('.//div[contains(@class, "p-name")]/a/em/text()')
		item['name'] = product_name[0].strip() if product_name else ''
		product_commit = product.xpath('.//div[contains(@class, "p-commit")]/strong/a/text()')
		item['commit'] = product_commit[0].strip() if product_commit else ''
		product_shop = product.xpath('.//div[contains(@class, "p-shop")]/span/a/text()')
		item['shop'] = product_shop[0].strip() if product_shop else ''
		yield item



def main():
	for page in range(100):
		# get_page(page+1)
		# print(page)
		page_source = get_page(page+1)
		products = parse_page(page_source)
		db = pymysql.connect(host='localhost',port=3306,user='root',password='123456',database='spider',charset='utf8')
		cursor = db.cursor()
		for product in products:
			sql = 'insert into jd_goods(img,price,name,commit,shop) values("%s","%s","%s","%s","%s")' %(product.get('img') if product.get('img') else '',product.get('price') if product.get('price') else '',
																										product.get('name') if product.get('name') else '',product.get('commit') if product.get('commit') else '',product.get('shop') if product.get('shop') else '')
			cursor.execute(sql)
			db.commit()
			print(sql)

			# print(product['name'])
			# print(product['price'])
			# print(product['img'])
			# print(product['commit'])
			# print(product['shop'])

if __name__ == '__main__':
	main()