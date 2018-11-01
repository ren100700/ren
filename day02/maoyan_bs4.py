import requests

from bs4 import BeautifulSoup
import pymysql

def get_one_page(offset):
	url = "https://http://maoyan.com/board/4?offset=%d" %offset
	headers = {
		"User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)"
	}
	response = requests.get(url, headers=headers)
	if response.status_code == 200:
		text = response.content.decode('utf-8')
		return text
	return None


def parse_soup(html):
	soup = BeautifulSoup(html, 'lxml')
