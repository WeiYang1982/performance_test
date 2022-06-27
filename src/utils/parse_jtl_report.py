#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:yang wei
@file:report_parser.py
@time:2022/06/27
"""

import pandas as pd


def test(data):
    return data.split("?")[0]


class SamplesParser:
    # def __init__(self):

    @staticmethod
    def get_samples(filepath):
        samples = pd.read_csv(filepath, encoding="utf-8")
        return samples

    def analytics_sample(self, data_frame):
        # 取path
        data_frame['URL'] = data_frame['URL'].apply(lambda x: x.split("?")[0] if pd.isnull(x) == False else x)
        data = data_frame.groupby(["label", "URL"], as_index=True).agg(
            {"elapsed": [pd.DataFrame.mean, pd.DataFrame.max, pd.DataFrame.min, len]})
        data['throughput'] = data_frame.groupby('label', as_index=True).apply(
            lambda x: len(data_frame) / (x['timeStamp'].max() - x['timeStamp'].min())) * 1000
        success_data = data_frame[data_frame['success'] == True]
        success_group = success_data.groupby('label').agg({'label': len})  #
        data['success_rate'] = success_group['label'] / data['elapsed']['len'] * 100
        data.columns = ['avg', 'max', 'min', 'len', 'throughput', 'success_rate']
        data = data.reset_index()
        return data.values.tolist()


if __name__ == '__main__':
    report_file = 'D:\\Code\\python_project\\performance_test\\tests\\report\\login.jtl'
    # data = pd.DataFrame()
    parser = SamplesParser()
    r = parser.get_samples(report_file)
    data = parser.analytics_sample(r)
    # samples =
    for d in data:
        print(d)
        print("***")

    pass
