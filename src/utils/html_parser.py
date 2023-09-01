#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:yang wei
@file:html_parser.py
@time:2022/07/08
"""
import json

from lxml import etree
import pandas as pd
import re


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

    def get_pd_report_summary_result(self):
        """
        返回样例：
        [{
            "level":{
                "MEDIUM":2
            },
            "package_name":"pkg:javascript/jquery@3.4.1",
            "image_name":"action"
        }]
        """
        table = self.html_content.xpath("//table[@id='summaryTable']/tr")
        result = []
        for i in range(1, len(table)):
            tmp_d = {}
            tr = table[i]
            td_list = tr.findall('td')

            level = td_list[3].xpath("./text()")[0].upper()
            count = int(td_list[4].xpath("./text()")[0])
            if level != '\xa0' and count != 0:
                try:
                    image_name = td_list[0].xpath("./*/text()")[0].split("@")[1]
                except IndexError:
                    image_name = td_list[0].xpath("./*/text()")[0]
                package_name = ";".join(td_list[2].xpath("./*/text()"))
                tmp_d.update({"module_name": image_name, "package_name": package_name})
                tmp_d['level'] = {level: count}
            if tmp_d != {}:
                result.append(tmp_d)
        return result

    def get_pd_detail_report(self):
        target_result = []
        vulnerabilities = self.html_content.xpath("//div[@class='subsectioncontent']")
        files = self.html_content.xpath("//h3[@class='subsectionheader standardsubsection']/text()")
        for i in range(len(files)):
            tmp_num = []
            # 取漏洞编号
            nums = vulnerabilities[i].xpath("./div[@class='subsectioncontent standardsubsection']/p/b/a")
            # not(*)   不包含下级节点
            # not(@class)  属性中不包含class
            # scores = vulnerabilities[i].xpath("./div[@class='subsectioncontent standardsubsection'][2]/ul/li[not(*) and not(@class)][1]/text()")
            # tmp_score = re.findall("[0-9]?[0-9].[0-9]", str(scores))
            # score_index = tmp_score.index(max(tmp_score))
            # level = scores[score_index][12:][:-6]
            # print(level)
            for num in nums:
                # tmp_scores = num.xpath("../../")
                tmp_num.append(num.text)
                print(num.text)
            module_name = files[i].split("@")[1]
            target_result.append({files[i]: tmp_num})
        return target_result


if __name__ == '__main__':
    html_file = "http://ci-bj.mycyclone.com/job/TestGroup/view/%E5%AE%89%E5%85%A8%E6%89%AB%E6%8F%8F/job/dependency_check/142/artifact/dependency-check-report.html"
    # html_content = etree.parse(html_file, etree.HTMLParser())
    parser = HTMLParser()
    parser.html_parser(html_file)
    summary = parser.get_pd_report_summary_result()
    # print(parser.total)
    detail = parser.get_pd_detail_report()
    for s in range(len(summary)):
        summary[s].update({"vulnerabilities": detail[s]})

    with open('result', 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False)
    # print(parser.case_summary_result)
    # pass
