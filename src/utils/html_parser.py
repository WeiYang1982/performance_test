#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:yang wei
@file:html_parser.py
@time:2022/07/08
"""
from lxml import etree


class HTMLParser:
    def __init__(self):
        self.total = 0
        self.case_detail_result = []
        self.case_summary_result = []
        self.html_content = None
        self.detail_keys = ["result", "type", "module", "caseName", "duration", "expect", "runTime"]
        self.summary_keys = ["module", "total", "passed", "failed"]

    def html_parser(self, html_file):
        self.html_content = etree.parse(html_file, etree.HTMLParser(encoding='utf-8'))

    def case_detail_parser(self):
        table = self.html_content.xpath("//table[@id='results-table']/tbody/tr[not(@class)]")
        for tr in table:
            td = tr.findall("td")
            # td = tr.xpath('./td')
            self.total += 1
            tmp_d = {}
            if len(td) == 0:
                continue
            for i in range(len(self.detail_keys)):
                tmp_d.update({self.detail_keys[i]: td[i].text})
            self.case_detail_result.append(tmp_d)

    def case_summary_parser(self):
        table = self.html_content.xpath("//table[@id='summary']/tr")
        for i in range(1, len(table)):
            tr = table[i]
            td = tr.findall('td')
            tmp_d = {}
            for i in range(len(self.summary_keys)):
                tmp_d.update({self.summary_keys[i]: td[i].text})
            self.case_summary_result.append(tmp_d)


if __name__ == '__main__':
    html_file = "D:\\Code\\python_project\\performance_test\\tests\\report\\performance_test_report.html"
    # html_content = etree.parse(html_file, etree.HTMLParser())
    parser = HTMLParser()
    parser.html_parser(html_file)
    parser.case_detail_parser()
    # print(parser.total)
    print(parser.case_detail_result)
    # print(parser.case_summary_result)
    pass
