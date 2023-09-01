#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:yang wei
@file:get_front_page_apis.py
@time:2022/10/20
"""
import os
import time
from urllib.parse import urlparse

from selenium.webdriver.common.by import By

from src.drivers.base_web_driver import BaseWebDriver
from src.pages.login_page import LoginPage


def get_front_page_apis(headless="False", server_host="http://172.19.192.44:30000", username="admin", password="admin", uri="/portal/News"):
    """
    使用selenium 抓取前端页面调用的请求
    """
    data = set()
    os.environ['driver_type'] = 'local'
    os.environ['headless'] = headless
    driver = BaseWebDriver().get_driver()
    driver.get(server_host + "/c-page/login")
    driver.delete_all_cookies()
    js = 'window.localStorage.clear();'
    driver.execute_script(js)
    time.sleep(5)
    login_page = LoginPage(driver)
    login_page.login(username, password)
    time.sleep(5)

    driver.get(server_host + uri)

    driver.refresh()
    time.sleep(20)
    frame = driver.find_elements(By.TAG_NAME, "iframe")
    if len(frame) > 0:
        driver.switch_to.frame(frame[0])
    r = driver.execute_script("return window.performance.getEntries();")
    for res in r:
        if res['entryType'] in ['navigation', 'resource']:
            if res['initiatorType'] in ["fetch", "xmlhttprequest"]:
                data.add(urlparse(res['name']).path)
    print(len(data))
    return list(data)


if __name__ == '__main__':
    os.environ['headless'] = 'False'
    get_front_page_apis(server_host="http://10.20.10.130")
    pass
