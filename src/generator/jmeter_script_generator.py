#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:yang wei
@file:jmeter_script_generator.py
@time:2022/10/13
"""
import json
import os

import jinja2
import jsonpath
import requests

from src.modules.get_front_page_apis import get_front_page_apis
from src.utils.config_manager import get_config, get_root_path


# 从接口自动化平台生成jmeter测试脚本
class JmeterScriptGeneratorFromPlatform:
    def __init__(self):
        self.module_id = "platform_test"
        self.tag_id = 8
        self.rest_host = get_config().get('global', 'rest_host')
        self.tag_uri = "/api/tag/all"
        self.category_uri = "/api/category/all"
        self.single_api_uri = "/api/singeApiInGroup"
        self.scenario_api_uri = "/api/scenarioInGroup"
        self.templates_path = get_root_path() + os.sep + "src" + os.sep + "resources"

    def get_tag_name(self, tag_id):
        """
        获取tag名称
        需要登录 暂时放弃
        """
        token = "eyJhbGciOiJIUzM4NCJ9.eyJqdGkiOiIxOTJiZjRhNy0wMmExLTQ1N2UtYjlkMS0wZDAzYWM4MDYyZDUiLCJzdWIiOiJ7XCJjaHNOYW1lXCI6XCLmnajlqIFcIixcImNyZWF0ZWRBdFwiOlwiMjAyMi0xMC0xMiAxNTo1NDo1MFwiLFwiaWRcIjozNCxcImxvZ2luTmFtZVwiOlwid2VpLnlhbmdcIixcInVwZGF0ZWRBdFwiOlwiMjAyMi0xMC0xMiAxNTo1NDo1MFwifSIsImlhdCI6MTY2NTU2MTYxNSwiZXhwIjoxNjY1NjQ4MDE1fQ.Z4FNJ9bfyyT1-jFNimfeGsIw6_Xm-SsBYXPjWlKvt2kjCO0ADtAy9s2aB93HeLDG"
        header = {"Authorization": "Bearer {}".format(token)}
        rest_url = self.rest_host + self.tag_uri
        res = requests.get(rest_url, headers=header).json()['data']
        target_data = {}
        for data in res:
            target_data[data['id']] = data['name']
        print(target_data)
        return target_data[tag_id]

    def get_single_api_data(self, created_by=None, tags=None, module_id=5):
        """
        获取单接口数据
        """
        rest_url = self.rest_host + self.single_api_uri
        params = {
            "createdBy": created_by,
            "tags": tags,
            "belongTo": module_id
        }
        self.module_id = module_id
        if tags is not None and tags != "":
            self.tag_id = tags
        res = requests.get(rest_url, params=params)
        if res.status_code == 200:
            print(res.text)
            return res.json()
        else:
            raise Exception("平台接口报错！！ res: {}".format(res.text))

    def jmeter_script_generator(self, case_list, template_name='need_login', output_file=None):
        """
        生成jmeter脚本文件
        """
        template_file = self.templates_path + os.sep + template_name + "_template.jmx"
        output_path = get_root_path() + os.sep + "target"
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        if output_file is None:
            output_file = "{}/{}_{}_{}_output.jmx".format(output_path, str(self.module_id), str(self.tag_id), template_name)
        else:
            output_file = "{}/{}_{}_{}_{}_output.jmx".format(output_path, str(self.module_id), str(self.tag_id), output_file, template_name)
        # case_list = jsonpath.jsonpath(api_data, "$.data")
        if case_list == [{}]:   # 判断是否是空内容
            raise Exception("接口数据为空，请检查！ res: {}".format(json.dumps(case_list)))
        else:
            f = open(template_file, 'r', encoding='utf-8')
            template_content = f.read()
            f.close()
            print(case_list)
            jmeter_script = jinja2.Template(template_content).render(case_list=case_list)
            with open(output_file, 'w', encoding='utf-8') as f:
                f.writelines(jmeter_script)
                f.close()


if __name__ == '__main__':
    json_file = "../../t.json"
    g = JmeterScriptGeneratorFromPlatform()
    # r = g.get_single_api_data(module_id=5)
    # with open(json_file, "r", encoding="utf-8") as f:
    #     content = f.read()
    # r = json.loads(content)
    # case_list = jsonpath.jsonpath(r, "$.data")
    process_id = "0c14b888580e492d9e9aea008000214e"
    pages = [
        {"page": '/pi/process/%s/analyze' % process_id, "case": "analyze"},
        # {"page": '/pi/process/%s/cases' % process_id, "case": "cases"},
        # {"page": '/pi/process/%s/comparison' % process_id, "case": "comparison"}
        ]
    for page in pages:
        case_list = get_front_page_apis(server_host="http://10.20.17.143", uri=page['page'])
    # case_list = ["http://aaa/a-api/aa"]
        g.jmeter_script_generator(case_list, template_name='front_page', output_file=page['case'])
    # print(r)
    # print(g.get_tag_name(1))
    pass
