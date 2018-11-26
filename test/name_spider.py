import requests
from lxml import etree
import pymysql

def get_page(url):
	headers = {
		"User-Agent":"Mozilla/4.0(compatible; MSIE 7.0;Windows NT 5.1; 360SE)"
	}
	response = requests.get(url,headers=headers)
	if response.status_code == 200:
		text = response.content.decode('utf-8')
		return text
		# 防中文乱码
		# return response.content.decode('utf-8')
	return None

def parse_page(html):
	etree_html = etree.HTML(html)
	names = etree_html.xpath('//div[@class="col-xs-12"]/a/text()')
	family_name = etree_html.xpath('//div[@class="navbar-collapse"]//ul[@class="nav navbar-nav"]/li[3]/a/text()')
	print(names)
	f1_name = family_name[0]
	print(f1_name)
	db = pymysql.connect(host='localhost', port=3306, user='root', password='123456', database='spider', charset='utf8')
	cursor = db.cursor()
	for name in names:
		print(name)
		sql = 'insert into name(name,family_name) values("%s","%s")' %(name,f1_name)
		cursor.execute(sql)
		db.commit()


def main():
	surname = ['qian','sun','li','zhou','wu','zheng','wang','feng','chen','chu','wei','shen','han','yang',
			   'zhu','qin','you','xu','he','lu','shi','zhang','kong','tzao','yan','hua','jin','wei1','tao','jiang1',
			   'qi','xie','zou','yu','bai','shui','dou','zhang1','yun','su','pan','ge','xi','fan','peng','lang','lu1',
			   'wei2','chang','ma','miao','feng1','hua1','fang','yu1','ren','yuan','liu','feng2','bao','shi1','tang','fei',
			   'lian','cen','xue','lei','he','ni','tang1','teng','yin','luo','hao','wu1','an','chang1','yue','yu2',
			   'shi2','fu','pi','bian','qi1','kang','wu2','yu3','yuan1','bu','gu','meng','ping','huang','he1','mu','xiao','yin1',
			   'yao','shao','zhan','wang1','qi2','mao','yu4','di','mi','bei','ming','zang','ji','fu1','cheng','dai','tan','song',
			   'mao1','pang','xiong','ji1','shu','qu','xiang','zhu1','dong','liang','du','ruan','lan','min','xi1','ji2','ma1','qiang',
			   'jia','lu2','lou','wei3','jiang2','tong','yan1','guo','mei','sheng','lin','diao','tzeng','xu1','chiu','lo1','gao',
			   'xia','tzai','tian','fan1','hu','ling','huo','yu5','wan','zhi','ke','zan','guan','lu3','mo','fang1','qiu','mao1','gan',
			   'xie1','ying','zong','ding','xuan','ben','deng','yi','shan','hang','hong','bao1','zhu2','zuo','shi3','tzui','ji3','niu',
			   'gong','cheng1','ji4','xing','hua2','pei','lu4','rong','ong','xun','yang1','fei1','zhen','qu1','jia1','feng3','zui','yi1',
			   'chu1','jin1','ji5','bing','mi1','song1','jing','duan','fu2','wu3','wu4','jiao','ba','gong1','mu1','kui','shan1','gu1','che',
			   'hou','mi2','peng1','quan','xi2','ban','yang2','qiu1','zhong','yi2','gong2','ning','qiu2','luan','bao2','gan1','tou','li1',
			   'rong1','zu','wu5','fu3','liu1','jing1','zhan1','shu1','long','ye','xing1','shu2','shao1','gao1','li2','ji6','pu','yin2','su1','bai1','why'
			   ]
	for i in range(5):
		offset = i+6
		for f_name in surname:
			url = 'http://' + (f_name) + '.resgain.net/name_list_%d.html' % offset
			html = get_page(url)
			parse_page(html)

if __name__ == '__main__':
	main()