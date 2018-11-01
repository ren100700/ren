import requests
from lxml import etree
import json
import pymysql


# 取页面HTML
def get_one_page():
	url = 'https://list.mogujie.com/search?callback=jQuery21107755214054895494_1540351139502&_version=8193&ratio=3%3A4&cKey=15&page=1&sort=pop&ad=0&fcid=50206&action=trousers&acm=3.mce.1_10_1hepw.109731.0.iOPIBr7mozQBm.pos_1-m_406086-sd_119-mf_15261_1047900-idx_0-mfs_10-dm1_5000&ptp=1._mf1_1239_15261.0.0.ZNBESUvF&_=1540351139503'
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
		html1 = html.split('(')[1:][0]
		html1 = html1.replace(');', '')
		return html1
	return None

def main():
	html = get_one_page()

	html_content = get_real_content(html)
	# print(html_content)
	result = json.loads(html_content)
	print(result['result']['wall']['docs'])
	# items = result['result']['wall']['docs']
	# print(result['status']['code'])
	# db = pymysql.connect(host='localhost',port=3306,user='root',password='123456',database='spider',charset='utf8')
	# cursor = db.cursor()
	# for item in items:
	# 	res={'tradeItemId':item['tradeItemId'],'itemType':item['itemType'],'img':item['img'],
	# 		 'link':item['link'],'title':item['title'],'orgPrice':item['orgPrice'],'sale':item['sale'],
	# 		 'cfav':item['cfav'],'price':item['price']
	# 		 }
	# 	sql='insert into mogujie(tradeItemId,itemType,img,link,title,orgPrice,sale,cfav,price) values("%s","%s","%s","%s","%s","%s","%s","%s","%s")' %(item['tradeItemId'],item['itemType'],item['img'],item['link'],item['title'],item['orgPrice'],item['sale'],item['cfav'],item['price'])
	# 	cursor.execute(sql)
	# 	db.commit()

if __name__ == '__main__':
	main()