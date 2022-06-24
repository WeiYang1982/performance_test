#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:yang wei
@file:performance_analytics.py
@time:2022/05/31
"""
# -*- coding: utf-8 -*-
import json
import os

import allure
import time

from src.drivers.base_web_driver import BaseWebDriver


class PageLoadAnalytics:

    def __init__(self, driver):
        self.verification_errors = []
        self.accept_next_alert = True
        # self.driver = BaseWebDriver().get_driver()
        self.driver = driver
        self.driver.implicitly_wait(30)
        self.gather_data_dict = []

    def test_untitled_test_case(self, name, url, number=1, expected_element=None):
        # 返回结果
        result = []
        # 读取压测数数据，返回加载结果！
        # for data in self.gather_data_dict:
        result_temp = {
            "UrlName": name,
            "Url": url,
            "number": number,
        }
        time.sleep(5)
        time_result = self.__get_page_load_time(url, int(number), expected_element)
        result_temp.update(time_result)
        result.append(result_temp)
        file_path = os.environ['allure_dir'] + "/collect_json"
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        with open(file_path + "/" + name + ".json", 'w', encoding='utf-8') as file:
            json.dump(result_temp, file, ensure_ascii=False)
        return result

    def __get_page_load_time(self, Url, number, expected_element):
        """
        网页无缓存的情况下进行加载速度测试
        :param Url: 加载的网址
        :param number: 加载次数
        :return:
        """
        driver = self.driver
        page_load_time = []
        dom_tree_time = []
        redirect_time = []
        DNS_search_time = []
        TTFB_time = []
        request_completed_time = []
        onload_event_time = []
        dom_ready_time = []
        white_page_time = []
        res_page = {}
        res_dom_ready = {}
        for i in range(number):
            # 调用浏览器打开一个新窗口
            # current_window = driver.window_handles[0]
            # driver.execute_script("window.open('','_blank');")
            # new_window = driver.window_handles[-1]
            # 窗口定位到新打开的窗口
            # driver.switch_to.window(new_window)

            driver.get(Url)
            driver.refresh()
            # WaitForElement.wait_until(driver, EC.presence_of_element_located(expected_element))
            time.sleep(10)

            full_log = driver.execute_script("let mytiming = window.performance.timing; return mytiming;")
            entries = driver.execute_script("return window.performance.getEntries()[0].duration;")
            allure.attach(body=json.dumps(full_log, ensure_ascii=False), name="PerformanceTiming_" + str(i),
                          attachment_type=allure.attachment_type.JSON)
            allure.attach(body=str(entries), name='load time', attachment_type=allure.attachment_type.TEXT)
            page_load_time.append(full_log['loadEventEnd'] - full_log['navigationStart'])
            dom_tree_time.append(full_log['domComplete'] - full_log['domInteractive'])
            TTFB_time.append(full_log['responseStart'] - full_log['navigationStart'])
            request_completed_time.append(full_log['responseEnd'] - full_log['responseStart'])
            dom_ready_time.append(full_log['domContentLoadedEventEnd'] - full_log['navigationStart'])
            redirect_time.append(full_log['redirectEnd'] - full_log['redirectStart'])
            DNS_search_time.append(full_log['domainLookupEnd'] - full_log['domainLookupStart'])
            onload_event_time.append(full_log['loadEventEnd'] - full_log['navigationStart'])
            white_page_time.append(full_log['responseStart'] - full_log['navigationStart'])
            time.sleep(0.5)
            # 关闭窗口
            # driver.execute_script("window.close();")
            # 窗口定位返回旧窗口
            # driver.switch_to.window(driver.window_handles[-1])

        res_page['max'] = max(page_load_time)
        res_page['min'] = min(page_load_time)
        res_page['avg'] = sum(page_load_time) / len(page_load_time)
        print(res_page)
        res_dom_ready['max'] = max(dom_ready_time)
        res_dom_ready['min'] = min(dom_ready_time)
        res_dom_ready['avg'] = sum(dom_ready_time) / len(dom_ready_time)

        dic = {
            "页面加载时间": res_page,
            "DOM加载时间": res_dom_ready,
            "解析DOM树结构的时间": {"max": max(dom_tree_time), "min": min(dom_tree_time),
                            "avg": sum(dom_tree_time) / len(dom_tree_time)},
            "读取页面第一个字节的时间": {"max": max(TTFB_time), "min": min(TTFB_time), "avg": sum(TTFB_time) / len(TTFB_time)},
            "request请求耗时": {"max": max(request_completed_time), "min": min(request_completed_time),
                            "avg": sum(request_completed_time) / len(request_completed_time)},
            "执行onload回调函数的时间": {"max": max(onload_event_time), "min": min(onload_event_time),
                                "avg": sum(onload_event_time) / len(onload_event_time)},
            # "重定向的时间": {"max": max(redirect_time), "min": min(redirect_time),
            #            "avg": sum(redirect_time) / len(redirect_time)},
            # "DNS查询耗时": {"max": max(DNS_search_time), "min": min(DNS_search_time),
            #             "avg": sum(DNS_search_time) / len(DNS_search_time)},
            "白屏时间": {"max": max(white_page_time), "min": min(white_page_time),
                     "avg": sum(white_page_time) / len(white_page_time)}
        }
        print(dic)
        return dic

    def tear_down(self):
        self.driver.close()


if __name__ == '__main__':
    os.environ['headless'] = 'False'
    data = [
        # {'UrlName': 'baidu', 'Url': 'https://www.baidu.com/', 'number': 2},
        {'UrlName': 'baidu', 'Url': 'http://172.19.192.44:30000/data-insight/lifeCycle', 'number': 2}
    ]
    driver = BaseWebDriver().get_driver()
    driver.get(data[0]["Url"])
    time.sleep(5)
    l = driver.execute_script("return window.performance.getEntries();")

    print(l[0]['duration'])
