#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:yang wei
@file:page_load.py
@time:2022/07/06
"""
import json
import os

import polling
import requests
from src.utils.config_manager import get_config


class PageLoad:
    def __init__(self, base_url):
        self.server = get_config().get('global', 'webpage_test_server')
        self.case_name = None
        self.timeout = 420
        self.base_url = base_url
        self.runs = 1
        self.f = "json"
        self.user_report = None
        self.json_report = None
        self.login_script = """
            clearCache
            lighthouse	            1
            logData	                0
            setEventName	        登录
            navigate	            {}/c-page/login
            sleep	                5
            keypressAndWait	        Tab
            typeAndWait	            {}
            keypressAndWait	        Tab
            typeAndWait	            {}
            keypressAndWait	        Enter
            sleep	                5
            clearCache
            logData	                1
        """
        self.case_template = """
            logData	                1
            setEventName	        {}
            navigate	            {}
        """

    @staticmethod
    def is_correct_response(response):
        return response.json()['statusCode'] == 200

    def test_runner(self, case_name, case_url, username='admin', password='admin', runs=None):
        self.case_name = case_name
        test_url = self.base_url + case_url
        case = self.case_template.format(case_name, test_url)
        script = self.login_script.format(self.base_url, username, password) + case
        params = {}
        params.update({"f": self.f})
        params.update({"runs": runs if runs is not None else self.runs})
        params.update({"script": script})
        params.update({"lighthouse": 1})
        params.update({"tcpdump": 1})
        params.update({"htmlbody": 1})
        params.update({"pngss": 1})
        params.update({"timeline": 1})
        # params.update({"mv": 1})
        # params.update({"video": 1})
        params.update({"browser_width": 1366})
        params.update({"browser_height": 768})
        # params.update({"type": "lighthouse"})
        response = requests.post(self.server, params=params)
        if response.status_code == 200:
            status_code = response.json()['statusCode']
            if status_code == 200:
                self.user_report = response.json()['data']['userUrl']
                self.json_report = response.json()['data']['jsonUrl']

    def report_parser(self, json_report):
        fully_loaded = first_contentful_paint = document_complete = speed_index = performance_score = 0
        response = polling.poll(lambda: requests.get(json_report), check_success=self.is_correct_response, step=15,
                                timeout=self.timeout)
        if 'data' in response.json():
            fully_loaded = response.json()['data']['average']['firstView']['fullyLoaded']
            document_complete = response.json()['data']['average']['firstView']['loadTime']
            first_contentful_paint = response.json()['data']['average']['firstView']['firstContentfulPaint']
            speed_index = response.json()['data']['average']['firstView']['SpeedIndex']
            # lighthouse 结果解析
            # first_contentful_paint = response.json()['data']['average']['firstView']['lighthouse.Performance.first-contentful-paint']
            # speed_index = response.json()['data']['average']['firstView']['lighthouse.Performance.speed-index']
            # performance_score = response.json()['data']['average']['firstView']['lighthouse.Performance']
        result = {"页面加载时间": {"avg": fully_loaded}, "speed_index": speed_index, "document_load_time": document_complete,
                  "first_contentful_paint": first_contentful_paint}  # , "performance_score": performance_score
        file_path = os.environ['allure_dir'] + "/collect_json"
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        with open(file_path + "/" + self.case_name + ".json", 'w', encoding='utf-8') as file:
            json.dump(result, file, ensure_ascii=False)
        return result


if __name__ == '__main__':
    p = PageLoad("http://10.20.18.196:30000")
    p.test_runner(case_name="COE", case_url="/market-place/backstagemanage/businesstag")
    print(p.json_report)
    print(p.user_report)
    print(p.report_parser(p.json_report))
    pass
