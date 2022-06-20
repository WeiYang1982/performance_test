#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:yang wei
@file:test_by_webpagetest.py
@time:2022/06/14
"""

import requests

base_script = """
    clearCache
    lighthouse	          1
    logData	              0
    setEventName	      登录
    navigate	          %LOGIN_URL%
    sleep	              5
    keypressAndWait	      Tab
    typeAndWait	          %USERNAME%
    keypressAndWait	      Tab
    typeAndWait	          %PASSWORD%
    keypressAndWait	      Enter
    sleep	              5
    clearCache
"""
case_template = """
    logData	              1
    setEventName	      %NAME%
    navigate	          %URL%
"""
url = "http://172.25.128.26:4000/runtest.php"

base_params = {
    "f": "json",
    "lighthouse": 1,
    "private": 0,
    "video": 1
}

headers = {
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json;charset=UTF-8'
}

test_data = [
    {"name": "数据大屏", "URL": "http://172.19.192.44:30000/data-insight/lifeCycle"},
    {"name": "个人工作台-数据看板", "URL": "http://172.19.192.44:30000/market-place/databoard"},
]

base_script = base_script.replace("%LOGIN_URL%", "http://172.19.192.44:30000").replace("%USERNAME%", "admin").replace("%PASSWORD%", "admin")
for d in test_data:
    base_script = base_script + case_template.replace("%NAME%", d['name']).replace("%URL%", d['URL'])

base_params.update({'script': base_script})

print(base_params)
response = requests.get(url, headers=headers, params=base_params)

print(response.text)

if __name__ == '__main__':
    pass
