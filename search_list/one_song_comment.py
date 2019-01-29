# -*- coding: utf-8 -*-
import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from lxml import etree

class song_comment():

    def __init__(self):
        self.browser = webdriver.Chrome()

    def parse_comment(self,link):
        try:
            self.browser.get(link)
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
        except Exception:
            pass