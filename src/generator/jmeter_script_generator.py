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

from src.utils.config_manager import get_config, get_root_path


class JmeterScriptGenerator:
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

    def jmeter_script_generator(self, api_data, script_type='need_login'):
        template_file = self.templates_path + os.sep + script_type + "_template.jmx"
        output_path = get_root_path() + os.sep + "target"
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        output_file = "{}/{}_{}_{}_output.jmx".format(output_path, str(self.module_id), str(self.tag_id), script_type)

        case_list = jsonpath.jsonpath(api_data, "$.data")
        if case_list == [{}]:   # 判断是否是空内容
            raise Exception("接口数据为空，请检查！ res: {}".format(json.dumps(api_data)))
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
    g = JmeterScriptGenerator()
    r = g.get_single_api_data(module_id=5)
    # with open(json_file, "r", encoding="utf-8") as f:
    #     content = f.read()
    # r = json.loads(content)

    g.jmeter_script_generator(r, script_type="need_login")
    # print(r)
    # print(g.get_tag_name(1))
    pass
