#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:yang wei
@file:element_is_exist.py
@time:2021/05/14
"""


def is_element_exist(element):
    flag = True
    try:
        element.is_displayed()
        flag = True
    except Exception:
        flag = False
    finally:
        return flag


if __name__ == '__main__':
    pass
