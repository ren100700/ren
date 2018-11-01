import requests
from lxml import etree
import json
import pymysql


# 取页面HTML
def get_one_page(url):
	headers =  {
		"User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)"
	}
	response = requests.get(url, headers=headers)
	if response.status_code == 200:
		text = response.content.decode('utf-8')
		return text
	return None


def get_real_content(html):
	# 获取json中的内容
	if html and len(html) > 128:
		i = html.index('(')
		html1 = html[i+1:]
		html2 = html1.replace(');', '')
		return html2
	return None


def main():
	db=pymysql.connect(host='localhost', port=3306, user='root', password='123456', database='spider',charset='utf8')
	flag = False
	while True:
		try:
			with open('page_number1.txt', 'r', encoding='utf8') as f:
				page = int(f.read())
			break
		except Exception as e:
			print(e)
			with open('page_number1.txt', 'w', encoding='utf8') as f:
				page_init = '1'
				f.write(page_init)

	while not flag:

		url = 'https://list.mogujie.com/search?callback=jQuery211029395870410478575_1540381443856&_version=8193&ratio=3%3A4&cKey=15&page='+str(page)+'&sort=pop&ad=0&fcid=51927&action=magic&acm=3.mce.1_10_178iu.18936.0.itmrvr7ota5gf.pos_6-m_168791-sd_119-mf_15261_1047900-idx_0-mfs_88-dm1_5000&ptp=1._mf1_1239_15261.0.0.oZdvrVaI&_=1540381443857'
		try:
			html = get_one_page(url)
		except Exception as e:
			with open('page_number1.txt', 'w', encoding='utf8') as f:
				f.write(str(page))
			print(e)
			break
		html_content = get_real_content(html)
		# print(html_content)
		result = json.loads(html_content)
		items = result['result']['wall']['docs']
		print(items)
		flag = result['result']['wall']['isEnd']
		cursor = db.cursor()
		# 'tradeItemId': item['tradeItemId'],
		for item in items:
			sql='insert into mogujie_kh(tradeItemId,itemType,img,link,title,orgPrice,sale,cfav,price) values("%s","%s","%s","%s","%s","%s","%s","%s","%s")' %(item.get('tradeItemId') if item.get('tradeItemId') else '',item.get('itemType') if item.get('itemType') else '',item.get('img') if item.get('img') else '',item.get('link') if item.get('link') else '',
																																							  item.get('title') if item.get('title') else '',item.get('orgPrice') if item.get('orgPrice') else '',item.get('sale') if item.get('sale') else '',item.get('cfav') if item.get('cfav') else '',item.get('price') if item.get('price') else '')
			cursor.execute(sql)
			db.commit()
			print(flag,page)
		if flag:
			with open('page_number1.txt', 'w', encoding='utf8') as f:
				f.write(str(page) + 'spider over')
		page += 1


if __name__ == '__main__':
	main()