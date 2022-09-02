#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:yang wei
@file:test_single_interface.py
@time:2022/06/23
"""

import allure
import pytest

stability_interface_threshold = 95

interfaces = [
    {'name': '数据', 'filename': 'analytics'},
    # {'name': '中控', 'filename': 'orch'},
    {'name': 'COE', 'filename': 'marketPlace'},
    {'name': 'COE', 'filename': 'personalWorkSpace'},
    {'name': '工单', 'filename': 'orderWork'},
]


@allure.feature("稳定性测试")
@allure.story("稳定性回归测试")
@pytest.mark.stability
def test_interface_stability(module, interface_name, interface_path, success_rate, expected, stability):
    assert success_rate >= expected
