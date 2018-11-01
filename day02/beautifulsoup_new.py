import requests

from bs4 import BeautifulSoup
import pymysql


# 取页面HTML
def get_one_page():
	url = "https://2018.sina.com.cn"
	headers = {
		"User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)"
	}
	response = requests.get(url, headers=headers)
	if response.status_code == 200:
		text = response.content.decode('utf-8')
		return text
	return None


def parse_soup(html):
	soup = BeautifulSoup(html,'lxml')
	# print(soup.prettify())
	# 获取网页标题
	# print(soup.title.string)
	# 获取head内容
	# print(soup.head)
	# 获取第一个P标签
	# print(soup.p)
	#获取节点名字
	# print(soup.title.name)
	print(soup.img.attrs["src"])


def savedata():
	db = pymysql.Connect(host='localhost',port=3306,user='root',password='123456',database='spider',charset='utf8')



def main():
	html = get_one_page()
	parse_soup(html)

if __name__ == '__main__':
	main()