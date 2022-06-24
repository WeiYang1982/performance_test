#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:yang wei
@file:get_allure_report.py
@time:2022/06/21
"""
import json

import jsonpath as jsonpath
import requests


class GetAllureReport:
    def __init__(self):
        self.result = []

    def get_summary_result(self, url):
        """
        提取对应jenkins job中的allure报告
        :param url: 需要获取报告的url
        :return:
        """
        url = url + "/allure/widgets/summary.json"
        json_body = requests.get(url)
        print(json_body.text)
        return json_body

    def get_duration_times_by_scenes(self, url):
        url = url + "/allure/data/behaviors.json"
        json_body = requests.get(url)
        sceneses = json_body.json()['children']
        for scenes in sceneses:
            sum = 0
            name = scenes['name']
            duration_time = jsonpath.jsonpath(scenes, "$.[*].duration")
            for time in duration_time:
                sum += time
            self.result.append({"scenes_name": name, "case_name": name, "duration": sum})
        return self.result

    def get_duration_times_by_case(self, url):
        url = url + "/allure/data/behaviors.json"
        json_body = requests.get(url)
        try:
            scenes_list = jsonpath.jsonpath(json_body.json(), '$.children[*]')
            for scenes in scenes_list:
                scenes_name = scenes['name']
            # scenes_list = jsonpath.jsonpath(json_body.json(), '$.children.*.children')
            # for scenes in scenes_list:
            #     scenes_name = jsonpath.jsonpath(scenes, "$.*.name")[0]
                for cases in scenes['children']:
                    if cases.__contains__("children"):
                        for case in cases['children']:
                            self.result.append({'scenes_name': scenes_name, 'case_name': case['name'], 'duration': case['time']['duration']})
                    else:
                        self.result.append({'scenes_name': scenes_name, 'case_name': cases['name'], 'duration': cases['time']['duration']})
        except Exception as e:
            print(e)
        return self.result


if __name__ == '__main__':
    url = "http://172.20.0.74:8080/job/TestGroup/view/RPA_automation/job/rpa_platform_interface_auto_test/"
    # url = "http://172.20.0.74:8080/job/Process/job/Process_AutoTest_UI/15"
    # GetAllureReport().get_summary_result(url)
    r = GetAllureReport().get_duration_times_by_case(url)
    print(r)
    pass
