#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:yang wei
@file:login_page.py
@time:2022/06/02
"""
from selenium.webdriver.common.by import By

from src.pages.page_template import BasePage
from src.utils.wait_for_element import WaitForElement


class LoginPage(BasePage):
    input_loc = (By.CLASS_NAME, 'ant-input')
    login_button_loc = (By.XPATH, "//button[@type='submit']")  # 默认登录界面
    # login_button_loc = (By.CLASS_NAME, "login-button")  # 开启内部登录

    @property
    def username(self):
        WaitForElement.wait_until(self.driver, self.EC.presence_of_element_located(self.input_loc))
        return self.locate_elements(self.input_loc)[0]

    @property
    def password(self):
        WaitForElement.wait_until(self.driver, self.EC.presence_of_element_located(self.input_loc))
        return self.locate_elements(self.input_loc)[1]

    @property
    def login_button(self):
        WaitForElement.wait_until(self.driver, self.EC.element_to_be_clickable(self.login_button_loc))
        return self.locate_element(self.login_button_loc)

    def login(self, username, password):
        self.username.send_keys(username)
        self.password.send_keys(password)
        self.login_button.click()
        # WaitForElement.wait_until(self.driver, self.EC.presence_of_element_located((By.CLASS_NAME, "userinfo")))


if __name__ == '__main__':
    pass
