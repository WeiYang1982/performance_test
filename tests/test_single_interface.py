#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:yang wei
@file:test_single_interface.py
@time:2022/06/23
"""

import allure
import pytest

single_interface_threshold = 1000


@allure.feature("性能测试")
@allure.story("单接口性能")
@pytest.mark.interface
@pytest.mark.all
def test_single_interface(module, interface_name, interface_path, duration, expected, performance):
    assert duration <= expected
