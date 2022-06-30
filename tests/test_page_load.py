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
    pytest.param('数据', '/data-insight/lifeCycle', page_load_threshold, marks=pytest.mark.test),  # 全生命周期
    pytest.param('数据', '/data-insight/demandDashboarde', page_load_threshold, marks=pytest.mark.test),  # 需求仪表盘
    pytest.param('数据', '/data-insight/controlDashboard', page_load_threshold, marks=pytest.mark.test),  # 控制仪表盘
    pytest.param('数据', '/data-insight/appDashboard', page_load_threshold, marks=pytest.mark.test),  # 应用仪表盘
    pytest.param('COE', '/market-place/databoard', page_load_threshold, marks=pytest.mark.test),  # 个人工作台_数据看板
    pytest.param('COE', '/orch/processTask/toDoList', page_load_threshold, marks=pytest.mark.test),  # 个人工作台_待办事项
    pytest.param('COE', '/orch/processTask/process', page_load_threshold, marks=pytest.mark.test),  # 个人工作台_我的流程
    pytest.param('COE', '/orch/processTask/execution', page_load_threshold, marks=pytest.mark.test),  # 个人工作台_运行记录
    pytest.param('COE', '/market-place/myrequirement', page_load_threshold, marks=pytest.mark.test),  # 个人工作台_我的需求
    pytest.param('COE', '/market-place/successcases', page_load_threshold, marks=pytest.mark.test),  # 卓越中心_成功案例
    pytest.param('COE', '/market-place/appmarket/hotrecommend', page_load_threshold, marks=pytest.mark.test),  # 卓越中心_应用市场
    pytest.param('COE', '/market-place/requiremanage', page_load_threshold, marks=pytest.mark.test),  # 卓越中心_需求管理
    pytest.param('COE', '/market-place/backstagemanage/casemanage', page_load_threshold, marks=pytest.mark.test),  # 卓越中心_案例管理
    pytest.param('COE', '/market-place/backstagemanage/appmanage/processmanage', page_load_threshold, marks=pytest.mark.test),  # 卓越中心_应用管理
    pytest.param('COE', '/market-place/backstagemanage/businesstag', page_load_threshold, marks=pytest.mark.test),  # 卓越中心_业务标签
    pytest.param('中控', '/orch/dashboards/home', page_load_threshold, marks=pytest.mark.test),  # 控制中心_仪表盘
    pytest.param('中控', '/orch/jobs/jobs/index', page_load_threshold, marks=pytest.mark.test),  # 控制中心_任务计划
    pytest.param('中控', '/orch/jobs/executions/', page_load_threshold, marks=pytest.mark.test),  # 控制中心_任务列表
    pytest.param('中控', '/orch/auditLog/job', page_load_threshold, marks=pytest.mark.test),  # 控制中心_任务日志
    pytest.param('中控', '/orch/jobs/manMachineTask/wait', page_load_threshold, marks=pytest.mark.test),  # 控制中心_人机任务
    pytest.param('中控', '/orch/watchdog/watchJob', page_load_threshold, marks=pytest.mark.test),  # 控制中心_watchdog
    pytest.param('中控', '/orch/jobs/robotProcesses', page_load_threshold, marks=pytest.mark.test),  # 控制中心_流程列表
    pytest.param('中控', '/orch/jobs/jobFlowableTemplate', page_load_threshold, marks=pytest.mark.test),  # 控制中心_编排模板
    pytest.param('中控', '/orch/jobs/serviceProcesses', page_load_threshold, marks=pytest.mark.test),  # 控制中心_流程服务
    pytest.param('中控', '/orch/robots/robots/index', page_load_threshold, marks=pytest.mark.test),  # 控制中心_机器人管理
    pytest.param('中控', '/orch/auditLog/robot', page_load_threshold, marks=pytest.mark.test),  # 控制中心_机器人日志
    pytest.param('中控', '/orch/robots/ledger', page_load_threshold, marks=pytest.mark.test),  # 控制中心_机器人台账
    pytest.param('中控', '/orch/robots/designer-management', page_load_threshold, marks=pytest.mark.test),  # 控制中心_设计器管理
    pytest.param('中控', '/orch/filemanagement/filemanagement', page_load_threshold, marks=pytest.mark.test),  # 控制中心_文件管理
    pytest.param('中控', '/orch/systemSettings/variables', page_load_threshold, marks=pytest.mark.test),  # 控制中心_变量管理
    pytest.param('中控', '/orch/jobs/datapool', page_load_threshold, marks=pytest.mark.test),  # 控制中心_数据队列
    pytest.param('中控', '/orch/businessLog/execution', page_load_threshold, marks=pytest.mark.test),  # 控制中心_业务日志
    pytest.param('中控', '/orch/deployment', page_load_threshold, marks=pytest.mark.test),  # 控制中心_安装包管理
    pytest.param('中控', '/orch/devices/servers', page_load_threshold, marks=pytest.mark.test),  # 控制中心_节点管理
    pytest.param('中控', '/orch/robots/labels/index', page_load_threshold, marks=pytest.mark.test),  # 控制中心_标签管理
    pytest.param('中控', '/orch/systemSettings/calendars', page_load_threshold, marks=pytest.mark.test),  # 控制中心_日历管理
    pytest.param('中控', '/orch/dailyReport', page_load_threshold, marks=pytest.mark.test),  # 控制中心_日报管理
    pytest.param('工单', '/webapp/tasklist/agency', page_load_threshold, marks=pytest.mark.test),  # 工单_我的待办
    pytest.param('工单', '/webapp/tasklist/complete', page_load_threshold, marks=pytest.mark.test),  # 工单_我的已办
    pytest.param('工单', '/webapp/tasklist/start', page_load_threshold, marks=pytest.mark.test),  # 工单_我发起的
    pytest.param('工单', '/webapp/tasklist/mystart', page_load_threshold, marks=pytest.mark.test),  # 工单_发起流程
    pytest.param('工单', '/webapp/positioning', page_load_threshold, marks=pytest.mark.test),  # 工单_数据管理
    pytest.param('工单', '/webapp/myProcess', page_load_threshold, marks=pytest.mark.test),  # 工单_我的流程
    pytest.param('工单', '/webapp/modeler', page_load_threshold, marks=pytest.mark.test)  # 工单_建模器
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
