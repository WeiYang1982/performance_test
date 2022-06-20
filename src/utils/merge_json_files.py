#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:yang wei
@file:merge_json_files.py
@time:2022/06/02
"""
import glob
import json
import os


def merge_json_files(path):
    result = []
    file_glob = os.path.join(path, "*.json")
    for f in glob.glob(file_glob):
        print(f)
        with open(f, 'r', encoding='utf-8') as file:
            for line in file.readlines():
                result.append(json.loads(line))
    if len(result) > 0:
        with open(path + "/result.json", 'w', encoding='utf-8') as f:
            print("write files")
            json.dump(result, f)
        return result


if __name__ == '__main__':
    import pandas as pd

    path = "D:\\Code\\python_project\\performance_test\\tests\\report\\collect_json"
    l = merge_json_files(path)
    d = pd.json_normalize(l, max_level=4)
    print(d)
    d.to_csv(path + "/aaa.xlsx")
    pass
