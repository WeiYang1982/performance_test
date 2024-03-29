#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:yang wei
@file:test_page_load.py
@time:2022/06/02
"""
import json
import os
import platform

import allure
import pytest
from selenium.webdriver.common.by import By
from src.modules.page_load_analytics import PageLoadAnalytics
from src.utils.config_manager import get_root_path

base_expected_element = (By.XPATH, "//ul[@role='menu']")

page_load_threshold = 2000

test_data = [
    pytest.param('数据_全生命周期', '/portal/News', page_load_threshold, marks=pytest.mark.test),
    # pytest.param('数据_全生命周期', '/data-insight/lifeCycle', page_load_threshold, marks=pytest.mark.test),
    # pytest.param('数据_需求仪表盘', '/data-insight/demandDashboarde', page_load_threshold, marks=pytest.mark.test),
    # pytest.param('数据_控制仪表盘', '/data-insight/controlDashboard', page_load_threshold, marks=pytest.mark.test),
    # pytest.param('数据_应用仪表盘', '/data-insight/appDashboard', page_load_threshold, marks=pytest.mark.test),
    # pytest.param('COE_个人工作台_数据看板', '/market-place/databoard', page_load_threshold, marks=pytest.mark.test),
    # pytest.param('COE_个人工作台_待办事项', '/orch/processTask/toDoList', page_load_threshold, marks=pytest.mark.test),
    # pytest.param('COE_个人工作台_我的流程', '/orch/processTask/process', page_load_threshold, marks=pytest.mark.test),
    # pytest.param('COE_个人工作台_运行记录', '/orch/processTask/execution', page_load_threshold, marks=pytest.mark.test),
    # pytest.param('COE_个人工作台_我的需求', '/market-place/myrequirement', page_load_threshold, marks=pytest.mark.test),
    # pytest.param('COE_卓越中心_成功案例', '/market-place/successcases', page_load_threshold, marks=pytest.mark.test),
    # pytest.param('COE_卓越中心_应用市场', '/market-place/appmarket/hotrecommend', page_load_threshold, marks=pytest.mark.test),
    # pytest.param('COE_卓越中心_需求管理', '/market-place/requiremanage', page_load_threshold, marks=pytest.mark.test),
    # pytest.param('COE_卓越中心_案例管理', '/market-place/backstagemanage/casemanage', page_load_threshold, marks=pytest.mark.test),
    # pytest.param('COE_卓越中心_应用管理', '/market-place/backstagemanage/appmanage/processmanage', page_load_threshold, marks=pytest.mark.test),
    # pytest.param('COE_卓越中心_业务标签', '/market-place/backstagemanage/businesstag', page_load_threshold, marks=pytest.mark.test),
    # pytest.param('中控_控制中心_仪表盘', '/orch/dashboards/home', page_load_threshold, marks=pytest.mark.test),
    # pytest.param('中控_控制中心_任务计划', '/orch/jobs/jobs/index', page_load_threshold, marks=pytest.mark.test),
    # pytest.param('中控_控制中心_任务列表', '/orch/jobs/executions/', page_load_threshold, marks=pytest.mark.test),
    # pytest.param('中控_控制中心_任务日志', '/orch/auditLog/job', page_load_threshold, marks=pytest.mark.test),
    # pytest.param('中控_控制中心_人机任务', '/orch/jobs/manMachineTask/wait', page_load_threshold, marks=pytest.mark.test),
    # pytest.param('中控_控制中心_watchdog', '/orch/watchdog/watchJob', page_load_threshold, marks=pytest.mark.test),
    # pytest.param('中控_控制中心_流程列表', '/orch/jobs/robotProcesses', page_load_threshold, marks=pytest.mark.test),
    # pytest.param('中控_控制中心_编排模板', '/orch/jobs/jobFlowableTemplate', page_load_threshold, marks=pytest.mark.test),
    # pytest.param('中控_控制中心_流程服务', '/orch/jobs/serviceProcesses', page_load_threshold, marks=pytest.mark.test),
    # pytest.param('中控_控制中心_机器人管理', '/orch/robots/robots/index', page_load_threshold, marks=pytest.mark.test),
    # pytest.param('中控_控制中心_机器人日志', '/orch/auditLog/robot', page_load_threshold, marks=pytest.mark.test),
    # pytest.param('中控_控制中心_机器人台账', '/orch/robots/ledger', page_load_threshold, marks=pytest.mark.test),
    # pytest.param('中控_控制中心_设计器管理', '/orch/robots/designer-management', page_load_threshold, marks=pytest.mark.test),
    # pytest.param('中控_控制中心_文件管理', '/orch/filemanagement/filemanagement', page_load_threshold, marks=pytest.mark.test),
    # pytest.param('中控_控制中心_变量管理', '/orch/systemSettings/variables', page_load_threshold, marks=pytest.mark.test),
    # pytest.param('中控_控制中心_数据队列', '/orch/jobs/datapool', page_load_threshold, marks=pytest.mark.test),
    # pytest.param('中控_控制中心_业务日志', '/orch/businessLog/execution', page_load_threshold, marks=pytest.mark.test),
    # pytest.param('中控_控制中心_安装包管理', '/orch/deployment', page_load_threshold, marks=pytest.mark.test),
    # pytest.param('中控_控制中心_节点管理', '/orch/devices/servers', page_load_threshold, marks=pytest.mark.test),
    # pytest.param('中控_控制中心_标签管理', '/orch/robots/labels/index', page_load_threshold, marks=pytest.mark.test),
    # pytest.param('中控_控制中心_日历管理', '/orch/systemSettings/calendars', page_load_threshold, marks=pytest.mark.test),
    # pytest.param('中控_控制中心_日报管理', '/orch/dailyReport', page_load_threshold, marks=pytest.mark.test),
    # pytest.param('工单_我的待办', '/webapp/tasklist/agency', page_load_threshold, marks=pytest.mark.test),
    # pytest.param('工单_我的已办', '/webapp/tasklist/complete', page_load_threshold, marks=pytest.mark.test),
    # pytest.param('工单_我发起的', '/webapp/tasklist/start', page_load_threshold, marks=pytest.mark.test),
    # pytest.param('工单_发起流程', '/webapp/tasklist/mystart', page_load_threshold, marks=pytest.mark.test),
    # pytest.param('工单_数据管理', '/webapp/positioning', page_load_threshold, marks=pytest.mark.test),
    # pytest.param('工单_我的流程', '/webapp/myProcess', page_load_threshold, marks=pytest.mark.test),
    # pytest.param('工单_建模器', '/webapp/modeler', page_load_threshold, marks=pytest.mark.test),

    # pytest.param('流程智能', '/pi/homepage', page_load_threshold, marks=pytest.mark.test),
    # pytest.param('系统设置_用户管理_用户管理', '/config-center/users', page_load_threshold, marks=pytest.mark.test),
    # pytest.param('系统设置_用户管理_角色管理', '/config-center/roles', page_load_threshold, marks=pytest.mark.test),
    # pytest.param('系统设置_用户管理_菜单管理', '/config-center/menus', page_load_threshold, marks=pytest.mark.test),
    # pytest.param('系统设置_用户管理_组织管理', '/config-center/organizations', page_load_threshold, marks=pytest.mark.test),
    # pytest.param('系统设置_通知中心_通知设置', '/config-center/alertSettings', page_load_threshold, marks=pytest.mark.test),
    # pytest.param('系统设置_审计日志', '/config-center/auditLog', page_load_threshold, marks=pytest.mark.test),
    # pytest.param('系统设置_个人中心_账户设置', '/config-center/accountSettings', page_load_threshold, marks=pytest.mark.test),
    # pytest.param('虚拟中控_任务管理_任务计划', '/vorch/JobPlan', page_load_threshold, marks=pytest.mark.test),
    # pytest.param('虚拟中控_任务管理_任务列表', '/vorch/Executions', page_load_threshold, marks=pytest.mark.test),
    # pytest.param('虚拟中控_流程管理_流程列表', '/vorch/ProcessList', page_load_threshold, marks=pytest.mark.test),
    # pytest.param('虚拟中控_机器人管理_执行器管理', '/vorch/ExecRobot', page_load_threshold, marks=pytest.mark.test),
    # pytest.param('虚拟中控_授权注册_厂商管理', '/vorch/SupplierRegistration', page_load_threshold, marks=pytest.mark.test),
    # pytest.param('虚拟中控_数据资产_变量管理', '/vorch/Variables', page_load_threshold, marks=pytest.mark.test),
]


@allure.feature("性能测试")
@allure.story("前端性能")
@allure.title("前端页面加载速度")
@pytest.mark.performance
@pytest.mark.all
@pytest.mark.parametrize("name, url, expected", test_data)
# @pytest.mark.usefixtures("driver")
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


# @allure.feature("性能测试")
# @allure.story("前端性能")
# @allure.title("前端页面加载速度")
# @pytest.mark.performance
# @pytest.mark.all
# @pytest.mark.parametrize("name, url, expected", test_data)
# def test_for_page_performance(name, url, expected):
#     from src.modules.page_load import PageLoad
#     client = PageLoad(os.environ['base_url'])
#     client.test_runner(case_name=name, case_url=url)
#     report_url = client.user_report
#     print(report_url)
#     result = client.report_parser(client.json_report)
#     result.update({"report": report_url})
#     allure.attach(body=json.dumps(result, ensure_ascii=False), name="加载时间",
#                   attachment_type=allure.attachment_type.JSON)
#     allure.attach(report_url, name="详细报告", attachment_type=allure.attachment_type.URI_LIST)
#     assert result['页面加载时间']['avg'] <= page_load_threshold


# @allure.feature("性能测试")
# @allure.story("前端性能")
# @allure.title("前端页面加载速度")
# @pytest.mark.performance
# @pytest.mark.all
# @pytest.mark.parametrize("name, url, expected", test_data)
# def test_for_page_performance(name, url, expected):
#     import subprocess as sp
#     from src.utils.config_manager import get_root_path
#     if platform.system().lower() == 'windows':
#         cmd = 'node -e "require(\\"%s\\").init(\\"%s\\", \\"%s\\")"' % ('./src/js/run_lighthouse_test.js', name, url)
#     else:
#         cmd = '/usr/bin/node -e "require(\\"%s\\").init(\\"%s\\", \\"%s\\")"' % ('./src/js/run_lighthouse_test.js', name, url)
#     os.chdir(get_root_path())
#     p1 = sp.Popen(cmd, shell=True, stdout=sp.PIPE, encoding='utf-8')
#     out = p1.communicate()[0]
#     # json_result = json.loads(out.replace("Promise { <pending> }", ""))
#     repost_file = get_root_path() + os.sep + 'report' + os.sep + 'collect_json' + os.sep + name + '.json'
#     with open(repost_file, 'r', encoding='utf-8') as f:
#         json_result = json.load(f)
#     allure.attach(body=json.dumps(json_result, ensure_ascii=False), name="加载时间",
#                   attachment_type=allure.attachment_type.JSON)
#     # assert json_result['性能'] >= 0.8
#     assert json_result['speed-index'] <= expected
#     os.chdir(os.getcwd())


if __name__ == '__main__':
    pass
