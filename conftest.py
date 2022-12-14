#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:admin
@file:conftest.py.py
@time:2021/05/13
"""
import glob
import json
import os
import shutil
import time
from datetime import datetime
from typing import Any, Callable, Optional

import jinja2
import pandas as pd
import pytest
import requests
from _pytest.fixtures import SubRequest
from py.xml import html

from src.drivers.base_web_driver import BaseWebDriver
from src.modules.jmeter_script_executor import JmeterScriptExecutor
from src.pages.login_page import LoginPage
from src.utils.capture_screenshot import ScreenShot
from src.utils.config_manager import get_config, get_root_path
from src.utils.file_manager import CountResult
from src.utils.get_file_path import get_file_path, get_dir_path
from src.utils.html_parser import HTMLParser
from src.utils.match_name import get_modules_name
from src.utils.parse_jtl_report import SamplesParser
from src.utils.send_email import SendEmail


ALLURE_ENVIRONMENT_PROPERTIES_FILE = "environment.properties"
ALLUREDIR_OPTION = "--alluredir"
case_result = []
test_result_list = []
global mark


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
    parser.addoption("--base_url", action="store", help="base url: None for default.")
    parser.addoption("--username", action="store", default="admin", help="login username: admin for default.")
    parser.addoption("--password", action="store", default="admin", help="login username: admin for default.")
    parser.addoption("--headless", action="store", default='False', help="browser type : headless or not.")
    parser.addoption("--mode", action="store", default='performance', help="test type: performance for default.")
    parser.addoption("--driver_type", action="store", default="local", help="driver type: chrome for default.")


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
def cenpprop(add_allure_environment_property: Callable, request) -> None:
    """
    自定义需要写入allure环境变量的内容
    :param set_env:
    :param add_allure_environment_property:
    :param request:
    :return:
    """
    global mark
    mark = request.config.getoption("-m")
    add_allure_environment_property("mark", mark)
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
    case_dic = {}
    file_name = None
    # report.description = str(item.function.__doc__)
    # print("report description" + report.description)
    if report.when == 'call':
        xfail = hasattr(report, 'wasxfail')
        report.extra = extra
        case_dic["id"] = report.nodeid
        case_dic["outcome"] = report.outcome
        case_result.append(case_dic)
        if (report.skipped and xfail) or (report.failed and not xfail):
            # 获取测试用例代码中webDriver参数来获取浏览器进行抓屏
            if 'web_driver' in locals().keys():
                file_name = '失败截图'
            pass
        if report.passed:
            file_name = '结束截图'
        try:
            ScreenShot.take_screenshot(web_driver, file_name)
        except Exception as e:
            print(e)


@pytest.mark.optionalhook
def pytest_html_report_title(report):
    global mark
    report.title = "RPA平台-非功能自动化测试报告:" + mark


# 修改Environment部分信息，配置测试报告环境信息
def pytest_configure(config):
    # 添加接口地址与项目名称
    config._metadata["项目名称"] = "RPA平台-九宫格Daily Build性能测试"
    config._metadata['测试环境'] = "{{ENV}}"
    config._metadata['mode'] = "{{MODE}}"
    config._metadata['开始时间'] = time.strftime('%Y-%m-%d %H:%M:%S')
    # config._metadata.pop("JAVA_HOME")
    config._metadata.pop("Packages")
    config._metadata.pop("Platform")
    config._metadata.pop("Plugins")
    config._metadata.pop("Python")


@pytest.mark.parametrize
def pytest_html_results_summary(prefix, summary, postfix):
    # from pytest_html import extras
    prefix.extend([html.p("owner: wei.yang")])
    prefix.extend([html.table(
        "{% for result in result_list %}",
        "{% if loop.first %}",
        html.tr(
            html.th("Module", style="padding: 5px;  border: 1px solid #E6E6E6;"),
            html.th("Total", style="padding: 5px;  border: 1px solid #E6E6E6;"),
            html.th("Passed", style="padding: 5px;  border: 1px solid #E6E6E6;"),
            html.th("Failed", style="padding: 5px;  border: 1px solid #E6E6E6;")
        ),
        "{% endif %}",
        html.tr(
            html.td("{{result.module}}", style="padding: 5px;  border: 1px solid #E6E6E6;"),
            html.td("{{result.total}}", style="padding: 5px;  border: 1px solid #E6E6E6;"),
            html.td("{{result.pass}}", style="padding: 5px;  border: 1px solid #E6E6E6;"),
            html.td("{{result.fail}}", style="padding: 5px;  border: 1px solid #E6E6E6;")
        ),
        "{% endfor %}",
        id='summary')])


@pytest.mark.optionalhook
def pytest_html_results_table_header(cells):
    cells.pop()
    cells.pop(-1)
    cells.pop(-1)
    cells.insert(1, html.th('Type'))
    cells.insert(2, html.th('Module'))
    cells.insert(3, html.th('CaseName'))
    cells.insert(4, html.th('{{TYPE}}', class_="sortable time", col="time"))
    cells.insert(5, html.th('Expected'))
    cells.insert(6, html.th("Execution Time", class_="sortable time", col="time"))


@pytest.mark.optionalhook
def pytest_html_results_table_row(report, cells):
    if not report.skipped:
        cells.pop()
        cells.pop(-1)
        cells.pop(-1)
        case_info = report.nodeid.split("[")[1].replace("]", "")
        module_name = report.nodeid.split("-")[0].split("[")[1]
        if "test_interface_scenes" in report.nodeid:
            expected = "<" + str(int(report.nodeid.split("-")[-1].replace("]", "")) / 1000) + "s"
            type_name = "后端(业务操作)性能"
            case_name = report.nodeid.split("-")[1]
            duration = report.nodeid.split("-")[-2]
            cells.insert(1, html.td(type_name))
            cells.insert(2, html.td(get_modules_name(module_name)))
            cells.insert(3, html.td(case_name))
            cells.insert(4, html.td(duration, class_="col-time"))
            cells.insert(5, html.td(expected))
            cells.insert(6, html.td(datetime.now(), class_="col-time"))
        elif "test_page_load" in report.nodeid:
            expected = "<" + str(int(report.nodeid.split("-")[-1].replace("]", "")) / 1000) + "s"
            type_name = "前端(页面加载)性能"
            case_name = report.nodeid.split("-")[1] + "-" + report.nodeid.split("-")[2].replace("]", "")
            json_file = glob.glob("*/collect_json/" + module_name + ".json")[0]
            with open(json_file, 'r', encoding='utf-8') as f:
                duration = json.load(f)['页面加载时间']['avg']
                # duration = json.load(f)['speed-index']
            cells.insert(1, html.td(type_name))
            cells.insert(2, html.td(get_modules_name(module_name)))
            cells.insert(3, html.td(case_name))
            cells.insert(4, html.td(duration, class_="col-time"))
            cells.insert(5, html.td(expected))
            cells.insert(6, html.td(datetime.now(), class_="col-time"))
        elif "test_single_interface" in report.nodeid:
            expected = "<=" + str(int(report.nodeid.split("-")[-2].replace("]", "")) / 1000) + "s"
            type_name = "后端(单接口)性能"
            case_name = report.nodeid.split("-")[1] + "——" + report.nodeid.split("-")[2]
            duration = report.nodeid.split("-")[-3]
            cells.insert(1, html.td(type_name))
            cells.insert(2, html.td(module_name))
            cells.insert(3, html.td(case_name))
            cells.insert(4, html.td(duration, class_="col-time"))
            cells.insert(5, html.td(expected))
            cells.insert(6, html.td(datetime.now(), class_="col-time"))
        elif "test_interface_stability" in report.nodeid:
            expected = ">=" + str(int(report.nodeid.split("-")[-2].replace("]", ""))) + "%"
            type_name = "稳定性回归测试"
            case_name = report.nodeid.split("-")[1] + "——" + report.nodeid.split("-")[2]
            success_rate = report.nodeid.split("-")[-3]
            cells.insert(1, html.td(type_name))
            cells.insert(2, html.td(module_name))
            cells.insert(3, html.td(case_name))
            cells.insert(4, html.td(success_rate))
            cells.insert(5, html.td(expected))
            cells.insert(6, html.td(datetime.now(), class_="col-time"))
        elif "test_dependency_scan" in report.nodeid:
            expected = report.nodeid.split("-")[-1].replace("]", "")
            type_name = "第三方依赖扫描"
            case_name = "-".join(report.nodeid.split("-")[1:][:-2])
            duration = report.nodeid.split("-")[-2]
            cells.insert(1, html.td(type_name))
            cells.insert(2, html.td(get_modules_name(module_name)))
            cells.insert(3, html.td(case_name))
            cells.insert(4, html.td(duration, class_="col-time"))
            cells.insert(5, html.td(expected))
            cells.insert(6, html.td(datetime.now(), class_="col-time"))
        # else:
        #     expected = "<" + str(int(report.nodeid.split("-")[-1].replace("]", "")) / 1000) + "s"
        #     type_name = "后端(单接口)性能"
        #     test_state = report.outcome
        #     cells.pop()
        #     cells.append(html.tr(
        #         "{% for module in module_list %}",
        #         html.tr(
        #             html.td(test_state, class_="col-result"),
        #             html.td(type_name),
        #             html.td("{{module.name}}"),
        #             html.td("{{module.path}}"),
        #             html.td("{{module.avg}}"),
        #             html.td(expected),
        #             html.td(datetime.now(), class_="col-time"),
        #             "{% endfor %}"))
        #     )


# def pytest_sessionstart(session):
#     session.config._metadata["测试环境"] = os.environ['env']


@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session):
    # 在测试用例执行完成后执行
    # summary_result = count_result(case_result)
    summary_result = CountResult().count_result(case_result)
    mail_info = {
        "host": get_config().get('mail', 'server_host'),
        "from_user": get_config().get('mail', 'from_user'),
        "from_pwd": get_config().get('mail', 'from_pwd'),
        "to_user": get_config().get('mail', 'to_user'),
        "cc_user": get_config().get('mail', 'cc_user'),
        "attachment_path": "",
        "attachment": "",
    }
    mail = SendEmail(mail_info)
    print(get_root_path())
    report_file = glob.glob('*/performance_test_report.html')[0]
    print(report_file)
    f = open(report_file, 'r', encoding='utf-8')
    html_mail = f.read()
    f.close()
    # exist, csv_file = get_file_path("result.csv")
    # module_list = []
    # if exist:
    #     case_list = pd.read_csv(csv_file, encoding='utf-8', header=None).values.tolist()
    #     for case in case_list:
    #         module_list.append({"name": case[0], "path": case[1], "avg": case[2]})
    report_type = "Duration(ms)" if os.environ['mode'] == 'performance' else "Success Rate(%)"
    html_mail = jinja2.Template(html_mail).render(result_list=summary_result, ENV=os.environ['env'], TYPE=report_type, MODE=os.environ['mode'])
    with open(report_file, 'w', encoding='utf-8') as f:
        f.writelines(html_mail)
        f.close()
    global mark
    title = "RPA平台-九宫格Daily Build性能自动化测试报告:" + mark
    mail.send_mail(title, html_mail)
    dir_exist, dir_path = get_dir_path('jmeter')
    if dir_exist:
        shutil.rmtree(dir_path)
    try:
        parser = HTMLParser()
        parser.html_parser(report_file)
        parser.case_detail_parser()
        parser.case_summary_parser()
        dict_body = {"title": "RPA平台-九宫格Daily Build性能测试报告", "autoCaseList": parser.case_detail_result,
                     "statistic": parser.case_summary_result, "workFlowId": os.environ['BUILD_ID'],
                     "environment": os.environ['env'], "platformURL": os.environ['base_url'],
                     "type": os.environ['mode']}
        print(dict_body)
        requests.post(url=get_config().get('global', 'mail_server'), json=dict_body)
    except Exception as e:
        print(e)
        pass


def pytest_generate_tests(metafunc):
    from tests.test_single_interface import single_interface_threshold
    from tests.test_interface_stability import interfaces, stability_interface_threshold
    global mark

    test_cases = []
    allure_dir = metafunc.config.getoption(ALLUREDIR_OPTION)
    mark = metafunc.config.getoption('-m')
    os.environ['env'] = metafunc.config.getoption("--env")
    os.environ['headless'] = metafunc.config.getoption("--headless")
    os.environ['mode'] = metafunc.config.getoption("--mode")
    os.environ['driver_type'] = metafunc.config.getoption("--driver_type")
    os.environ['base_url'] = get_config().get(os.environ['env'], 'login_url') if metafunc.config.getoption("--base_url") is None else metafunc.config.getoption("--base_url")
    os.environ['username'] = get_config().get(os.environ['env'], 'username') if metafunc.config.getoption("--username") == get_config().get(os.environ['env'], 'username') else metafunc.config.getoption("--username")
    os.environ['password'] = get_config().get(os.environ['env'], 'password') if metafunc.config.getoption("--password") == get_config().get(os.environ['env'], 'password') else metafunc.config.getoption("--password")
    os.environ['allure_dir'] = allure_dir

    if 'stability' in mark and 'stability' in metafunc.fixturenames:
        test_type = 'stability'
    elif ('interface' in mark or 'all' == mark) and 'performance' in metafunc.fixturenames:
        test_type = 'performance'
    else:
        test_type = None

    if test_type is not None:
        num_threads = get_config().get(test_type, 'interface_test_num_threads')
        exec_time = get_config().get(test_type, 'interface_test_exec_time')
        curr_dir = os.getcwd()
        executor = JmeterScriptExecutor()
        parser = SamplesParser()
        for interface in interfaces:
            result_file = executor.jmeter_executor(interface['filename'], num_threads, exec_time)
            os.chdir(curr_dir)
            result_file = glob.glob(result_file)[0]
            datas = parser.get_samples(result_file)
            cases = parser.analytics_sample(datas)
            #  'name', 'path', 'avg', 'max', 'min', 'len', 'throughput', 'success_rate'
            if test_type == 'stability':
                for case in cases:
                    test_cases.append(pytest.param(interface['name'], case[0].replace("-", "_"), case[1], case[-1], stability_interface_threshold, test_type))
            elif test_type == 'performance':
                for case in cases:
                    test_cases.append(pytest.param(interface['name'], case[0].replace("-", "_"), case[1], case[2], single_interface_threshold, test_type))
        if test_type == 'stability':
            metafunc.parametrize("module, interface_name, interface_path, success_rate, expected, stability", test_cases)
        elif test_type == 'performance':
            metafunc.parametrize("module, interface_name, interface_path, duration, expected, performance", test_cases)


if __name__ == '__main__':
    summary_result = [{"module": "aaa", "total": 1, "pass": 2, "fail": 3}]

    # with open("D:\\Code\\python_project\\interface_scenes_test\\tests\\report\\performance_test_report.html", 'r',
    #           encoding='utf-8') as f:
    #     html = jinja2.Template(f.read()).render(summary_result)
    #     with open(os.path.join('D:\\Code\\python_project\\interface_scenes_test\\tests\\report\\test.html'), 'w',
    #               encoding='utf-8') as f:
    #         f.writelines(html)
    #         f.close()
    # for root, dirs, files in os.walk(get_root_path()):
    #     if "result.csv" in files:
    #         print(root)
    #         print(files)
    csv_file = 'D:\\Code\\python_project\\performance_test\\tests\\report\\jmeter\\result.csv'
    l = pd.read_csv(csv_file, encoding='utf-8', header=None).values.tolist()
    print(l)
    pass
