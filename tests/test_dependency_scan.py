#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:yang wei
@file:test_dependency_scan.py
@time:2022/09/01
"""
import allure
import pytest

from src.modules.jenkins_tools import JenkinsTools
from src.utils.html_parser import HTMLParser

dict_leader = {
    "be-automation": "金鑫",
    "common-service-gw": "金鑫",
    "common-service": "金鑫",
    "orch-compat": "金鑫",
    "license-service": "上海",
    "trigger-service": "金鑫",
    "expose-service": "金鑫",
    "fe-orchestrator-orch": "金鑫",
    "fe-orchestrator-system": "金鑫",
    "fe-common-page": "金鑫",
    "fe-common-main": "金鑫",
    "fe-automation": "范军",
    "fe-webapp": "范军",
    "fe-modeler": "金鑫",
    "fe-appstudio": "金鑫",
    "fe-dashboard": "刘振杰",
    "portal-web": "金鑫",
    "compat-web": "金鑫",
    "ws-orch-web": "范军",
    "fe_data_insight_bi": "刘振杰",
    "gateway": "金鑫",
    "manager-service": "金鑫",
    "vorch-trigger-service": "金鑫",
    "workflow-service": "金鑫",
    "portal-service": "金鑫",
    "ws-orch-service": "金鑫",
    "be_data_insight_bi": "刘振杰",
    "be-data-insights": "刘振杰",
    "be-data-insights-etl": "刘振杰",
    "be-account": "范军",
    "be-camunda": "范军",
    "be-dataservice": "范军",
    "be-fileservice": "范军",
    "be-hyperpm": "范军",
    "be-inventory": "范军",
    "be-roe": "范军",
    "portal-manager": "金鑫",
    "fe-config-center": "金鑫",
    "cpm-ui-react": "张治明",
    "fe-appstore": "金鑫",
    "platform_manager": "金鑫",
    "vorch-api": "金鑫",
    "vorch-core": "金鑫",
    "vorch-trigger": "金鑫",
    "vorch-adapter": "金鑫",
    "user-defined-algorithm": "王建",
    "ai-studio-debugging": "王建",
    "template_proxy": "王建",
    "cpm-rest": "张治明",
    "gui": "张治明"
}

threshold = ["HIGH", "CRITICAL"]

job_name = 'TestGroup/dependency_check'


def get_testcases(job_name):
    test_cases = []
    job_url = JenkinsTools().get_job_last_build_url(job_name)
    dp_report_url = job_url + "artifact/dependency-check-report.html"
    parser = HTMLParser()
    parser.html_parser(dp_report_url)
    result = parser.get_pd_report_summary_result()
    owner = '未知'
    for case in result:
        if case['image_name'] in dict_leader:
            owner = dict_leader[case['image_name']]
        test_cases.append(pytest.param(owner, case['image_name'] + "-" + case['package_name'], str(case['level']), ";".join(threshold)))
    return test_cases


interface_scenes = get_testcases(job_name)


@allure.feature("安全测试")
@allure.story("扫描第三方依赖包")
@pytest.mark.dependency
@pytest.mark.all
@pytest.mark.parametrize('owner, image_name, summary_result, threshold_levels', interface_scenes)
def test_dependency_scan(owner, image_name, summary_result, threshold_levels):

    levels = threshold_levels.split(";")
    for k, v in eval(summary_result).items():
        assert k not in levels


if __name__ == '__main__':
    # html_file = "D:\\Code\\python_project\\performance_test\\report\\dependency-check-report.html"
    # parser = HTMLParser()
    # parser.html_parser(html_file)
    # summary_result = parser.get_pd_report_summary_result()
    # for k, v in summary_result.items():
    #     if k in dict_leader:
    #         summary_result[k]['OWNER'] = dict_leader[k]
    # print(str(summary_result))
    # import json
    # with open('result', 'w', encoding='utf-8') as f:
    #     json.dump(dict_leader, f, ensure_ascii=False)
    pass
