#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:yang wei
@file:test_page_load.py
@time:2022/06/02
"""
import json
import os

import allure
import pytest
from selenium.webdriver.common.by import By
from src.modules.page_load_analytics import PageLoadAnalytics

base_expected_element = (By.XPATH, "//ul[@role='menu']")

page_load_threshold = 2000

test_data = [
    pytest.param('数据', '/data-insight/lifeCycle', page_load_threshold, marks=pytest.mark.test),
    pytest.param('COE', '/market-place/databoard', page_load_threshold, marks=pytest.mark.test), #个人工作台_数据看板
    pytest.param('COE', '/orch/processTask/toDoList', page_load_threshold, marks=pytest.mark.test), # 个人工作台_待办事项
    pytest.param('COE', '/orch/processTask/process', page_load_threshold, marks=pytest.mark.test), # 个人工作台_我的流程
    pytest.param('COE', '/orch/processTask/execution', page_load_threshold, marks=pytest.mark.test), # 个人工作台_运行记录
    pytest.param('COE', '/market-place/myrequirement', page_load_threshold, marks=pytest.mark.test), # 个人工作台_我的需求
    pytest.param('COE', '/market-place/successcases', page_load_threshold, marks=pytest.mark.test), # 卓越中心_成功案例
    pytest.param('COE', '/market-place/appmarket/hotrecommend', page_load_threshold, marks=pytest.mark.test), # 卓越中心_应用市场
    pytest.param('COE', '/market-place/requiremanage', page_load_threshold, marks=pytest.mark.test), # 卓越中心_需求管理
    pytest.param('COE', '/market-place/backstagemanage/casemanage', page_load_threshold, marks=pytest.mark.test), # 卓越中心_案例管理
    pytest.param('COE', '/market-place/backstagemanage/appmanage/processmanage', page_load_threshold, marks=pytest.mark.test), # 卓越中心_应用管理
    pytest.param('COE', '/market-place/backstagemanage/businesstag', page_load_threshold, marks=pytest.mark.test), # 卓越中心_业务标签
    pytest.param('工单', '/webapp/tasklist/agency', page_load_threshold, marks=pytest.mark.test)
]


@allure.feature("性能测试")
@allure.story("前端性能")
@allure.title("前端页面加载速度")
@pytest.mark.performance
@pytest.mark.all
@pytest.mark.parametrize("name, url, expected", test_data)
@pytest.mark.usefixtures("driver")
@pytest.mark.usefixtures("login")
def test_for_page_performance(driver, name, url, expected):
    """
    测试前端页面加载速度
    """
    analytics = PageLoadAnalytics(driver)
    test_result = analytics.test_untitled_test_case(name, os.environ['base_url'] + url)
    allure.dynamic.title(name)
    load_time = test_result[0]['页面加载时间']['avg']
    print(load_time)
    assert load_time <= expected
    allure.attach(body=json.dumps(test_result, ensure_ascii=False), name="加载时间",
                  attachment_type=allure.attachment_type.JSON)


if __name__ == '__main__':
    pass
