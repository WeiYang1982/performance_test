#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:yang wei
@file:test_interface_scenes.py
@time:2022/06/21
"""
import os

import pytest
import allure

from src.modules.get_allure_report import GetAllureReport
from src.modules.jenkins_tools import JenkinsTools


job_names = [
    # 'TestGroup/rpa_platform_interface_auto_test',
    'Process/Process_AutoTest_UI'
]

interface_threshold = 5000


def get_testcases(job_names):
    test_cases = []
    for job_name in job_names:
        job_url = JenkinsTools().get_job_last_build_url(job_name)
        r = GetAllureReport().get_duration_times_by_case(job_url)
        for case in r:
            test_cases.append(pytest.param(case['scenes_name'].replace("-", "_"), case['case_name'].replace("-", "_"), case['duration'], interface_threshold))
    return test_cases


interface_scenes = get_testcases(job_names)


@allure.feature("性能测试")
@allure.story("测试混合场景下接口性能")
@pytest.mark.scenes
@pytest.mark.all
@pytest.mark.parametrize('scenes_name, case_name, duration, expected', interface_scenes)
def test_interface_scenes(scenes_name, case_name, duration, expected):
    assert duration <= expected


if __name__ == '__main__':
    pass
