import requests
import random
import time
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lxml import etree
from PIL import Image

#取浏览器窗口全图
def get_big_img():
	# 向下滑动300距离
	# 截取浏览器窗口全图
	for x in range(300):
		screenshot = Image.open('./image/%s' %("%d.png" %(x+1)))
		for i in range(4):
			crop_img = screenshot.crop((76*i,0,76*(i+1),76))
			file_name = '%d_%d.png' %((x+1),(i+1))
			crop_img.save('./image2/'+file_name)


def main():
	get_big_img()


if __name__ == "__main__":
	main()
