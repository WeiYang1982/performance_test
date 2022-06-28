#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:yang wei
@file:get_file_path.py
@time:2022/06/28
"""
import os

from src.utils.config_manager import get_root_path


def get_file_path(file_name):
    for root, dirs, files in os.walk(get_root_path()):
        if file_name in files:
            # print(root)
            # print(files)
            return True, root + os.sep + file_name
    return False, None


def get_dir_path(dir_name):
    for root, dirs, files in os.walk(get_root_path()):
        if dir_name in dirs:
            # print(root)
            # print(files)
            return True, root + os.sep + dir_name
    return False, None


if __name__ == '__main__':
    print(get_dir_path("jmeter"))
    pass
