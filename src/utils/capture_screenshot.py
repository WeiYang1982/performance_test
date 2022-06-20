#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:yang wei
@file:capture_screenshot.py
@time:2021/05/13
"""
import os
import uuid
import allure
from src.utils.config_manager import get_root_path

screenshots_dir = get_root_path() + os.sep + 'report' + os.sep + 'images'


class ScreenShot:

    @staticmethod
    def create_dic(file_name):
        path = os.path.dirname(file_name)
        if not os.path.exists(path):
            os.makedirs(path)

    @staticmethod
    def take_screenshot(webdriver, test_name=None):
        image_file = test_name if test_name is not None else str(uuid.uuid1())
        screenshot_file_path = "{}/{}.png".format(os.environ['allure_dir'] if os.environ['allure_dir'] is not None else screenshots_dir, image_file)
        ScreenShot.create_dic(screenshot_file_path)
        webdriver.save_screenshot(screenshot_file_path)
        allure.attach.file(screenshot_file_path, attachment_type=allure.attachment_type.PNG, name=image_file)
        return screenshot_file_path


if __name__ == '__main__':
    pass
