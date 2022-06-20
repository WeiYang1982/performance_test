#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:admin
@file:conftest.py.py
@time:2021/05/13
"""
import json
import os
import time
from datetime import datetime

import allure
import pytest
from typing import Any, Callable, Optional, Union

from _pytest.config import Config
from _pytest.fixtures import SubRequest
from _pytest.reports import CollectReport, TestReport
from py.xml import html
from selenium import webdriver
from selenium.webdriver.support.event_firing_webdriver import EventFiringWebDriver
from webdriver_manager.chrome import ChromeDriverManager

from src.drivers.base_web_driver import BaseWebDriver
from src.drivers.event_listener import EventListener
from src.pages.login_page import LoginPage
from src.utils.capture_screenshot import ScreenShot
from src.utils.config_manager import get_config

ALLURE_ENVIRONMENT_PROPERTIES_FILE = "environment.properties"
ALLUREDIR_OPTION = "--alluredir"

global web_driver


@pytest.fixture
def driver():
    """
    打开浏览器
    :return:
    """
    global web_driver
    web_driver = BaseWebDriver().get_driver()
    yield web_driver
    web_driver.quit()


def pytest_addoption(parser):
    """
    解析命令行参数 --env
    :param parser:
    :return:
    """
    parser.addoption("--env", action="store", default="test", help="Test environment: test for default.")
    parser.addoption("--driver_type", action="store", default="local", help="driver type: chrome for default.")
    parser.addoption("--headless", action="store", default='False', help="driver type: chrome for default.")


@pytest.fixture(scope="session", autouse=True)
def set_env(request):
    """
    根据命令行参数--env，设置环境变量
    :param request:
    :return:
    """
    allure_dir = request.config.getoption(ALLUREDIR_OPTION)
    os.environ['env'] = request.config.getoption("--env")
    os.environ['driver_type'] = request.config.getoption("--driver_type")
    os.environ['headless'] = request.config.getoption("--headless")
    os.environ['base_url'] = get_config().get(os.environ['env'], 'login_url')
    os.environ['username'] = get_config().get(os.environ['env'], 'username')
    os.environ['password'] = get_config().get(os.environ['env'], 'password')
    os.environ['allure_dir'] = allure_dir


@pytest.fixture()
@pytest.mark.usefixtures("driver")
def login(driver):
    driver.get(os.environ['base_url'] + "/c-page/login")
    driver.delete_all_cookies()
    js = 'window.localStorage.clear();'
    driver.execute_script(js)
    time.sleep(5)
    login_page = LoginPage(driver)
    login_page.login(os.environ['username'], os.environ['password'])
    time.sleep(5)


@pytest.fixture(scope="session", autouse=True)
def add_allure_environment_property(request: SubRequest) -> Optional[Callable]:
    """
    自动生成allure环境变量
    :param request:
    :return:
    """
    environment_properties = dict()

    def maker(key: str, value: Any):
        environment_properties.update({key: value})

    yield maker
    allure_dir = request.config.getoption(ALLUREDIR_OPTION)
    if not allure_dir or not os.path.isdir(allure_dir) or not environment_properties:
        return
    allure_env_path = os.path.join(allure_dir, ALLURE_ENVIRONMENT_PROPERTIES_FILE)
    with open(allure_env_path, 'w', encoding='utf-8') as _f:
        data = '\n'.join([f'{variable}={value}' for variable, value in environment_properties.items()])
        _f.write(data)


@pytest.fixture(scope="session", autouse=True)
def cenpprop(add_allure_environment_property: Callable, request, set_env) -> None:
    """
    自定义需要写入allure环境变量的内容
    :param set_env:
    :param add_allure_environment_property:
    :param request:
    :return:
    """
    add_allure_environment_property("mark", request.config.getoption("-m"))
    add_allure_environment_property("base_url", os.environ['base_url'])
    add_allure_environment_property("env", os.environ['env'])


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    """
    测试失败时，自动截图
    """
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])
    global web_driver
    global result
    file_name = None
    # report.description = str(item.function.__doc__)
    # print("report description" + report.description)
    if report.when == 'call':
        xfail = hasattr(report, 'wasxfail')
        # 判断用例是否失败或者xfail跳过的测试
        if (report.skipped and xfail) or (report.failed and not xfail):
            # 获取测试用例代码中webDriver参数来获取浏览器进行抓屏
            if web_driver:
                file_name = '失败截图'
            pass
        if report.passed:
            file_name = '结束截图'
        ScreenShot.take_screenshot(web_driver, file_name)
        report.extra = extra
    # report.nodeid = report.nodeid.encode("utf-8").decode("unicode_escape")
    # report.nodeid = report.nodeid
    # def pytest_sessionstart(session):
    #     file_path = os.environ['allure_dir'] + "/collect_json"
    #     if not os.path.exists(file_path):
    #         os.makedirs(file_path)

    # def pytest_sessionfinish(session, exitstatus):
    from src.utils.merge_json_files import merge_json_files
    import pandas as pd
    # file_path = os.environ['allure_dir'] + "/collect_json"
    # json_object = merge_json_files(file_path)
    # data = pd.json_normalize(json_object, max_level=4)
    # data.to_excel(file_path + "/result.xlsx")


@pytest.mark.parametrize
def pytest_html_results_summary(prefix, summary, postfix):
    prefix.extend([html.p("owner: wei.yang")])


@pytest.mark.optionalhook
def pytest_html_results_table_header(cells):
    # cells.insert(1, html.th("Description"))
    cells.insert(1, html.th('Test'))
    cells.insert(2, html.th("Time", class_="sortable time", col="time"))
    cells.pop(-3)


@pytest.mark.optionalhook
def pytest_html_results_table_row(report, cells):
    # cells.insert(1, html.td(report.description))
    cells.insert(1, html.td(report.nodeid))
    cells.insert(2, html.td(datetime.now(), class_="col-time"))
    cells.pop(-3)


if __name__ == '__main__':
    pass
