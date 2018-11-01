import requests
import json
import re


def get_page(offset):
	url = 'http://maoyan.com/board/4?offset=%d' %offset
	headers = {
		"User-Agent":"Mozilla/4.0(compatible; MSIE 7.0;Windows NT 5.1; 360SE)"
	}
	response = requests.get(url,headers=headers)
	if response.status_code == 200:
		return response.text
		# 防中文乱码
		# return response.content.decode('utf-8')
	return None


def parse_page(html):
	# 主演
	pattern2 = re.compile('<p class="star">(.*?)</p>',re.S)
	# 上映时间
	pattern3 = re.compile('<p class="releasetime">(.*?)</p>',re.S)
	# 电影名
	pattern1 = re.compile('movieId.*?>.*?<img.*?<img.*?alt="(.*?)" class.*?', re.S)
	# 图片地址
	pattern5 = re.compile('movieId.*?>.*?<img.*?<img.*?src="(.*?)"', re.S)
	# 电影排行
	pattern4 = re.compile("<dd>.*?board-index.*?>(.*?)</i>", re.S)
	name_items = re.findall(pattern1,html)
	actor_items = re.findall(pattern2,html)
	time_items = re.findall(pattern3,html)
	rank_items = re.findall(pattern4,html)
	address_items = re.findall(pattern5,html)
	movies = []
	print(name_items)
	for i in range(len(actor_items)):
		one_movie = {}
		one_movie['name'] = name_items[i].strip()
		one_movie['actor'] = actor_items[i].strip()
		one_movie['time'] = time_items[i].strip()
		one_movie['rank'] = rank_items[i].strip()
		movies.append(one_movie)
	return movies


def write_img(url):
	arr = url.split('@')
	filename = arr[0].split('/')[-1]
	with open('./image/%s' % filename,'wb')as f:
		response = requests.get(url)
		f.write(response.content)


def get_all_page():
	items={}
	for i in range(10):
		offset = i * 10
		html = get_page(offset)
		# items = parse_page(html)
		movies = parse_page(html)
		page_name = 'page%d' % (i+1)
		items[page_name]=movies
		str = json.dumps(items,ensure_ascii=False)
	with open('./maoyan.json','w',encoding='utf-8')as f:
		f.write(str)
		# print(items)
		# for item in items:
		# 	print(item.strip())
		# 	# write_img(item.strip())


def write_json():
	with open('./maoyantop100.json', 'w', encoding='utf-8') as f:
		# 写数据
		w_content = [
			{'name': 'a1', 'age': 18},
			{'name': 'a2', 'age': 20}
		]
		json.dump(w_content, f)


def main():
	# url = 'http://maoyan.com/board/4'
	# html = get_page(url)
	# items = parse_page(html)
	# # print(html)
	# # print(items)
	# for item initems:
	# 	print(item.strip())
	# 	write_img(item.strip())
	get_all_page()
	# write_json()

if __name__ == '__main__':
	main()