# -*- coding: utf-8 -*-
import codecs
import json
import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from lxml import etree
import pymongo
import requests
import urllib.request
# from wangyiyun.author_home_page.get_author import *


class Selenium_wangyi():
    def __init__(self):
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 10)
        self.client = pymongo.MongoClient('localhost',27017)
        self.db = self.client['wangyiyun']
        self.base_url = 'https://music.163.com'
        self.Audio_url = 'http://music.163.com/song/media/outer/url?id={}'

    def get_link(self,link):
        try:
            self.browser.get(link)
            f = self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
            print(f)
            self.browser.switch_to.frame(f)
            time.sleep(1)
            doc = etree.HTML(self.browser.page_source)
            # divs = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='j-flag']//tr")))
            divs =doc.xpath("//div[@id='song-list-pre-cache']//div[@class='j-flag']//tr")
            for div in divs:
                # name = self.wait.until(EC.presence_of_element_located((By.XPATH, "./td[@class='w4']/div/a/@title")))[0]
                name = div.xpath("./td[@class='']//b/@title")[0]
                song_link = self.base_url + div.xpath("./td[@class='']//span/a/@href")[0]
                print(name,song_link)
                id = song_link.split('=')[1]
                Audio_link = self.Audio_url.format(id)
                item = {'name':name,'link':Audio_link}
                self.insert_json(item)
                self.browser.get(song_link)
                self.parse_comment()
            return self.browser
        except TimeoutException as e:
            print('Error Timeout',e.args)
            return self.get_link(link)

    def parse_comment(self):
        try:
            time.sleep(1.5)
            windows = self.browser.window_handles
            # 切换到当前最新打开的窗口
            self.browser.switch_to.window(windows[-1])
            # print(self.browser.page_source)
            f = self.browser.find_element_by_tag_name("iframe")
            self.browser.switch_to.frame(f)
            doc = etree.HTML(self.browser.page_source)
            item = {}
            item['song_name'] = doc.xpath("//div[@class='tit']/em[@class='f-ff2']/text()")[0]
            item['author'] = doc.xpath("//p[@class='des s-fc4']/span/@title")[0]
            for div in doc.xpath("//div[@class='m-cmmt']/div[@class='cmmts j-flag']/div"):
                c = div.xpath("./div[@class='cntwrap']//div[@class='cnt f-brk']/text()")
                item['comment'] = ''.join([i.strip('：') for i in c])
                print(item)
                self.insert_mongo(item)
        except Exception as e:
            print('Error',e.args)
        try:
            links = self.browser.find_elements_by_tag_name("a")
            for link in links:
                if link.text == '下一页':
                    link.click()
                    return self.parse_comment()
        except StaleElementReferenceException:
            links = self.browser.find_elements_by_tag_name("a")
            for link in links:
                if link.text == '下一页':
                    link.click()
                    return self.parse_comment()

    def insert_json(self,value):
        with open("./item.json", "a+", encoding="utf-8") as file:
            line = json.dumps(value, ensure_ascii=False) + "\n"
            file.write(line)
            file.close()

    def insert_mongo(self,item):
        if self.db['wangyi_comment'].update({'comment':item['comment']},{'$set': item},True):
            print('Save to Mongo ', item['author'])
        else:
            print('No to Mongo',item['author'])

    def parse_Audio(self,link):
        with open('./Audio.txt','a+',encoding='utf-8') as f:
            f.write(link + '\n')
            f.close()

    def run(self,link):
        self.get_link(link)

if __name__ == '__main__':
    wangyi = Selenium_wangyi()
    wangyi.run("http://.........")

