#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:yang wei
@file:match_name.py
@time:2022/06/23
"""
import difflib

module_keywords = {
    "中控": ["控制中心", "中控"],
    "COE": ["需求", "流程", "个人工作台", "卓越", "卓越中心", "后台管理", "应用市场"],
    "数据": ["数据概览", "数据大屏", "数据"],
    "工单": ["工单"]
}


def get_modules_name(origin_name):
    result = []
    for key, values in module_keywords.items():
        tmp_name = origin_name
        match_result = difflib.get_close_matches(tmp_name, values, 1, cutoff=0.286)
        if len(match_result) >= 1:
            result.append(key)
    print(result)
    if len(result) >= 1:
        return result[0]
    else:
        return origin_name


if __name__ == '__main__':
    print(get_modules_name("中控"))
    pass
