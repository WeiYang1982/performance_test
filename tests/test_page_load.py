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
import pandas as pd
import pytest
from py.xml import html
from selenium.webdriver.common.by import By
from src.page_load_analytics import PageLoadAnalytics

base_expected_element = (By.XPATH, "//ul[@role='menu']")

page_load_threshold = 500

test_data = [
    # pytest.param('数据大屏', '/data-insight/lifeCycle', page_load_threshold,  marks=pytest.mark.test),
    # pytest.param('个人工作台-数据看板', '/market-place/databoard', page_load_threshold,  marks=pytest.mark.test),
    # pytest.param('个人工作台-待办事项', '/orch/processTask/toDoList', page_load_threshold,  marks=pytest.mark.test),
    # pytest.param('个人工作台-我的流程', '/orch/processTask/process', page_load_threshold,  marks=pytest.mark.test),
    # pytest.param('个人工作台-运行记录', '/orch/processTask/execution', page_load_threshold,  marks=pytest.mark.test),
    # pytest.param('个人工作台-我的需求', '/market-place/myrequirement', page_load_threshold,  marks=pytest.mark.test),
    pytest.param('卓越中心-成功案例', '/market-place/successcases', page_load_threshold, marks=pytest.mark.test),
    # pytest.param('卓越中心-应用市场', '/market-place/appmarket/hotrecommend', page_load_threshold,  marks=pytest.mark.test),
    # pytest.param('卓越中心-需求管理', '/market-place/requiremanage', page_load_threshold,  marks=pytest.mark.test),
    # pytest.param('卓越中心-案例管理', '/market-place/backstagemanage/casemanage', page_load_threshold,  marks=pytest.mark.test),
    # pytest.param('卓越中心-应用管理', '/market-place/backstagemanage/appmanage/processmanage', page_load_threshold, marks=pytest.mark.test),
    # pytest.param('卓越中心-业务标签', '/market-place/backstagemanage/businesstag', page_load_threshold, marks=pytest.mark.test),
    # pytest.param('工单', '/webapp/tasklist/agency', page_load_threshold, marks=pytest.mark.test)
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
    # result = pd.json_normalize(test_result, max_level=3)
    # print(result)
    # metrics = driver.execute_cdp_cmd("Performance.getMetrics", {})
    # print(metrics)
    # for m in metrics:
    #     print(m)
    print(test_result)
    load_time = test_result[0]['页面加载时间']['avg']
    print(load_time)
    assert load_time <= expected
    allure.attach(body=json.dumps(test_result, ensure_ascii=False), name="加载时间",
                  attachment_type=allure.attachment_type.JSON)


if __name__ == '__main__':
    pass
