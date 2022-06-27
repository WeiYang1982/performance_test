#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:yang wei
@file:test_single_interface.py
@time:2022/06/23
"""
import allure
import pytest
from src.utils.parse_jtl_report import SamplesParser
from src.modules.jmeter_script_executor import JmeterScriptExecutor

scripts_names = [
    pytest.param('COMMON', 'login'),
    # 'Process/Process_AutoTest_UI'
]
num_threads = 1
exec_time = 10
interface_threshold = 1000


# def get_testcases(scripts):
#     test_cases = []
#     executor = JmeterScriptExecutor()
#     parser = SamplesParser()
#     for script in scripts:
#         result_file = executor.jmeter_executor(script['script'], num_threads, exec_time)
#         datas = parser.get_samples(result_file)
#         cases = parser.analytics_sample(datas)
#         for case in cases:
#             test_cases.append(pytest.param(script['module_name'], case['URL'], case['avg'], interface_threshold))
#     return test_cases


# interfaces = get_testcases(scripts_names)


@allure.feature("性能测试")
@allure.story("单接口性能")
@pytest.mark.interface
@pytest.mark.all
@pytest.mark.parametrize('module_name, case_name', scripts_names)
def test_interface_scenes(module_name, case_name):
    executor = JmeterScriptExecutor()
    parser = SamplesParser()
    result_file = executor.jmeter_executor(case_name, num_threads, exec_time)
    datas = parser.get_samples(result_file)
    cases = parser.analytics_sample(datas)
    for case in cases:
        assert case['avg'] <= interface_threshold
