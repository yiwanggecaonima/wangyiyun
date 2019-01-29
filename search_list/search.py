# -*- coding: utf-8 -*-
from urllib.parse import quote
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
from wangyiyun.search_list.one_song_comment import song_comment

class Search():
    def __init__(self):
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 10)
        self.client = pymongo.MongoClient('localhost', 27017)
        self.db = self.client['wangyiyun']
        self.comment = song_comment()
        self.base_url = 'https://music.163.com'
        self.url = 'https://music.163.com/#/search/m/?order=hot&cat=%E5%85%A8%E9%83%A8&limit=435&offset=435&s={}&type=1'

    def search(self):
        keys = input("Search Key:")
        self.browser.get(self.url.format(quote(keys)))
        return self.browser

    def search_result(self):
        try:
            time.sleep(1.5)
            windows = self.browser.window_handles
            # 切换到当前最新打开的窗口
            self.browser.switch_to.window(windows[-1])
            f = self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
            print(f)
            self.browser.switch_to.frame(f)
            time.sleep(1)
            doc = etree.HTML(self.browser.page_source)
            divs = doc.xpath("//div[@class='n-srchrst']/div[@class='srchsongst']/div")
            for div in divs:
                link = self.base_url + div.xpath("./div[@class='td w0']//div[@class='text']/a/@href")[0]
                self.comment.parse_comment(link)
            try:
                # if doc.xpath("//*[@class='zbtn znxt js-n-1548726589048 js-disabled']"):
                #     print("Page exhaustion ...")
                #     pass
                links = self.browser.find_elements_by_tag_name("a")
                for link in links:
                    if link.text == '下一页':
                        link.click()
                        return self.search_result()
            except StaleElementReferenceException:
                links = self.browser.find_elements_by_tag_name("a")
                for link in links:
                    if link.text == '下一页':
                        link.click()
                        return self.search_result()
            except Exception:
                print("Page exhaustion ...")
                pass

        except Exception as e:
            print('Error',e.args)
            return self.search_result()

if __name__ == '__main__':
    search = Search()
    search.search()
    search.search_result()

