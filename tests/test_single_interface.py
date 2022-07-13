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
from src.utils.config_manager import get_config


interface_threshold = 1000

test_data = [
    pytest.param('中控', 'login', interface_threshold, marks=pytest.mark.test),
    pytest.param('数据', 'analytics', interface_threshold, marks=pytest.mark.test),
    pytest.param('中控', 'orch', interface_threshold, marks=pytest.mark.test),
    pytest.param('卓越中心', 'marketPlace', interface_threshold, marks=pytest.mark.test),
    pytest.param('个人工作台', 'personalWorkSpace', interface_threshold, marks=pytest.mark.test),
    pytest.param('工单', 'orderWork', interface_threshold, marks=pytest.mark.test),
]


@allure.feature("性能测试")
@allure.story("单接口性能")
@pytest.mark.interface
@pytest.mark.all
@pytest.mark.parametrize('module_name, case_name, expected', test_data)
def test_single_interface(module_name, case_name, expected):
    mode = os.environ['mode'] if os.environ['mode'] == 'performance' else 'stability'
    num_threads = get_config().get(mode, 'interface_test_num_threads')
    exec_time = get_config().get(mode, 'interface_test_exec_time')
    curr_dir = os.getcwd()
    executor = JmeterScriptExecutor()
    parser = SamplesParser()
    result_file = executor.jmeter_executor(case_name, num_threads, exec_time)
    os.chdir(curr_dir)
    result_file = glob.glob(result_file)[0]
    datas = parser.get_samples(result_file)
    cases = parser.analytics_sample(datas)
    for case in cases:
        allure.attach(body=str(case), name=case[0], attachment_type=allure.attachment_type.TEXT)
        if mode == 'performance':
            assert case[2] <= interface_threshold
        else:
            assert case[-1] >= 0.95
