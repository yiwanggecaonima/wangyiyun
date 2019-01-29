import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from lxml import etree
import pymongo
import requests
import urllib.request
from wangyiyun.author_home_page.author_page import Selenium_wangyi

class Author():
    def __init__(self):
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 10)
        self.start_url = 'https://music.163.com/#/discover/artist'
        self.base_url = 'https://music.163.com'
        self.comment = Selenium_wangyi()
        self.lst = []

    def get_author(self):
        self.browser.get(self.start_url)
        f = self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
        print(f)
        self.browser.switch_to.frame(f)
        time.sleep(1)
        doc = etree.HTML(self.browser.page_source)
        li_list = doc.xpath("//div[@class='g-wrap']/div/ul/li")
        for li in li_list:
            if li.xpath("./p/a/text()"):
                author = li.xpath("./p/a/@href")[0]
            else:
                author = li.xpath("./a/@href")[0]
            url = 'https://music.163.com' + author
            self.comment.run(url)


if __name__ == '__main__':
    author = Author()
    author.get_author()

