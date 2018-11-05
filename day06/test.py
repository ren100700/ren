import re

import requests

def get_page():
	for i in range(300):
		url = 'http://www.1kkk.com/image3.ashx?t=154080123600%d' %i
		headers = {
			"User-Agent":"Mozilla/4.0(compatible; MSIE 7.0;Windows NT 5.1; 360SE)"
		}
		response = requests.get(url,headers=headers)
		if response.status_code == 200:
			return response.content
		return None




def write_img():
	image= get_page()
	with open('./image/%s' %"aaa.png" ,'wb')as f:
		f.write(image)


def main():
	for i in range(300):
		url = 'http://www.1kkk.com/image3.ashx?t=1540801236000'
		headers = {
			"User-Agent": "Mozilla/4.0(compatible; MSIE 7.0;Windows NT 5.1; 360SE)"
		}
		response = requests.get(url, headers=headers)
		if response.status_code == 200:
			image =  response.content
		with open('./image/%s' %("%d.png" %(i+1)), 'wb')as f:
			f.write(image)
		print(i+1)


if __name__ == '__main__':
	main()