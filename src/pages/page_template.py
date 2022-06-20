#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:admin
@file:page_template.py
@time:2021/05/10
"""
import logging
import time
from selenium.webdriver.support import expected_conditions as EC


class BasePage(object):
    def __init__(self, driver):
        self.validate_page(driver)
        self.driver = driver
        self.log = logging.getLogger(__name__)
        self.EC = EC

    @classmethod
    def validate_page(cls, driver):
        wait_time = 0
        while driver.execute_script('return document.readyState;') != 'complete' and wait_time < 10:
            wait_time += 0.1
            time.sleep(0.1)
        print('Load Complete.')
        return

    def locate_element(self, locator):
        return self.driver.find_element(*locator)

    def locate_elements(self, locator):
        return self.driver.find_elements(*locator)


if __name__ == '__main__':
    pass
