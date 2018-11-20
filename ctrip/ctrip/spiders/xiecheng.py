# -*- coding: utf-8 -*-
import scrapy
from ctrip.items import CtripItem
from scrapy import Request, Spider

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lxml import etree
import time

class XiechengSpider(scrapy.Spider):
    name = 'xiecheng'
    allowed_domains = ['ctrip.com']
    start_urls = ['http://hotels.ctrip.com/hotel/chengdu28#ctm_ref=hod_hp_sb_lst']

    # def start_requests(self):
    #     url = 'http://hotels.ctrip.com/hotel/chengdu28#ctm_ref=hod_hp_sb_lst'
    #     for page in range(1, 10):
    #         print('*' * 20)
    #         yield Request(url=url, callback=self.parse, meta={'page': page}, dont_filter=True)

    def parse_one_page(self, page_source):
        etree_html = etree.HTML(page_source)

        results = etree_html.xpath('//div[@id="hotel_list"]//ul[@class="hotel_item"]')
        result_list = []
        for hotel in results:
            ctrip_item = CtripItem()
            ctrip_item['hotel_name'] = hotel.xpath('.//h2[@class="hotel_name"]/a/@title')
            result_list.append(ctrip_item)
        return result_list
 
    def parse(self, response):
        url = 'http://hotels.ctrip.com/hotel/chengdu28#ctm_ref=hod_hp_sb_lst'
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('user-agent="Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36"')

        # chrome_options.add_argument('--headless')
        browser = webdriver.Chrome(chrome_options=chrome_options)
        # browser = webdriver.Chrome()
        browser.set_window_size(1400, 1000)
        # self.browser.set_page_load_timeout(timeout)
        # 显式等待 针对某个节点的等待
        timeout = 10
        wait = WebDriverWait(browser, timeout)

        browser.get(url)

        city_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#txtCity')))
        city_input.clear()
        city_input.send_keys('上海')

        checkin_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#txtCheckIn')))
        checkin_input.clear()
        checkin_input.send_keys('2018-12-07')

        checkout_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#txtCheckOut')))
        checkout_input.clear()
        checkout_input.send_keys('2018-12-10')

        roomcount_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_roomCount')))
        roomcount_input.click()

        time.sleep(3)
        room3_click = wait.until(EC.element_to_be_clickable((By.XPATH, '//ul[@id="J_roomCountList"]/li[3]')))
        room3_click.click()

        member_click = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="J_RoomGuestInfoTxt"]')))
        member_click.click()

        adult_click = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[@id="J_AdultCount"]//i[@class="icon_numplus"]')))
        adult_click.click()
        adult_click.click()
        adult_click.click()

        baby_click = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[@id="J_ChildCount"]//i[@class="icon_numplus"]')))
        baby_click.click()
        baby_click.click()
        
        time.sleep(5)
        member_ok_click = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@id="J_RoomGuestInfoBtnOK"]')))
        member_ok_click.click()

        search_click = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="btnSearch"]')))
        search_click.click()


        time.sleep(5)
        page_source = browser.page_source

        result_list = self.parse_one_page(page_source)
        for item in result_list:
            yield item

        ad_click = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@class="fl_wrap_close"]')))
        ad_click.click()

        for page in range(10):
            for i in range(6):
                str_js = 'var step = document.body.scrollHeight / 8; window.scrollTo(0, step * %d)' % (i + 1)
                browser.execute_script(str_js)
                time.sleep(1)

            # str_js = 'window.scrollTo(0, document.body.scrollHeight - 400)'
            # browser.execute_script(str_js)
            # time.sleep(5)

            time.sleep(5)

            page_click = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class="c_page_list layoutfix"]/a[%d]' % (page + 2))))
            page_click.click()


            time.sleep(5)
            page_source = browser.page_source
            result_list = self.parse_one_page(page_source)
            
            for item in result_list:
                yield item


