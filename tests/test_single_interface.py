#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:yang wei
@file:test_single_interface.py
@time:2022/06/23
"""
import glob
import os

import allure
import pytest

from src.modules.jmeter_script_executor import JmeterScriptExecutor
from src.utils.parse_jtl_report import SamplesParser

num_threads = 100
exec_time = 120
interface_threshold = 1000

test_data = [
    pytest.param('中控', 'login', interface_threshold, marks=pytest.mark.test),
    pytest.param('数据', 'analytics', interface_threshold, marks=pytest.mark.test),
]


@allure.feature("性能测试")
@allure.story("单接口性能")
@pytest.mark.interface
@pytest.mark.all
@pytest.mark.parametrize('module_name, case_name, expected', test_data)
def test_single_interface(module_name, case_name, expected):
    curr_dir = os.getcwd()
    executor = JmeterScriptExecutor()
    parser = SamplesParser()
    result_file = executor.jmeter_executor(case_name, num_threads, exec_time)
    os.chdir(curr_dir)
    result_file = glob.glob(result_file)[0]
    datas = parser.get_samples(result_file)
    cases = parser.analytics_sample(datas)
    for case in cases:
        assert case[2] <= interface_threshold
