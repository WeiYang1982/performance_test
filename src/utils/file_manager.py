from src.utils.match_name import get_modules_name

module_dict = {
    "coe": "COE",
    "data": "数据",
    "orch": "中控",
    "order": "工单",
    "other": "其他"
}


class CountResult:
    def __init__(self):
        self.module = self.__dict__
        self.result = []
        for k, v in module_dict.items():
            self.module[k + '_pass'] = 0
            self.module[k + '_fail'] = 0
            self.module[k] = 0

    def count_result(self, reports):
        for report in reports:
            module_name = get_modules_name(report['id'].split("-")[0].split("[")[1])

            if module_name in module_dict.values():
                k = [k for k, v in module_dict.items() if v == module_name][0]
                self.module[k] += 1
                if report['outcome'] == 'passed':
                    self.module[k + '_pass'] += 1
            else:
                self.module['other'] += 1
                if report['outcome'] == 'passed':
                    self.module['other_pass'] += 1
        for k, v in module_dict.items():
            self.module[k + '_fail'] = self.module[k] - self.module[k + '_pass']
            self.result.append({"module": v, "total": self.module[k], "pass": self.module[k + '_pass'], "fail": self.module[k + '_fail']})
        return self.result


def count_result(case_result):
    """
    处理结果
    :param case_result: 结果list
    :return:
    """
    coe = coe_pass = data = data_pass = orch = orch_pass = order = order_pass = 0

    for i in case_result:
        module_name = get_modules_name(i['id'].split("-")[0].split("[")[1])
        if 'COE' in module_name:
            # i['id'].split("-")
            coe += 1
            if i['outcome'] == 'passed':
                coe_pass += 1
        if '数据' in module_name:
            data += 1
            if i['outcome'] == 'passed':
                data_pass += 1
        if '中控' in module_name:
            orch += 1
            if i['outcome'] == 'passed':
                orch_pass += 1
        if '工单' in module_name:
            order += 1
            if i['outcome'] == 'passed':
                order_pass += 1

    coe_fail = 0 if not coe - coe_pass else coe - coe_pass
    data_fail = 0 if not data - data_pass else data - data_pass
    orch_fail = 0 if not orch - orch_pass else orch - orch_pass
    order_fail = 0 if not order - order_pass else order - order_pass

    result = [{"module": "COE", "total": coe, "pass": coe_pass, "fail": coe_fail},
              {"module": "数据", "total": data, "pass": data_pass, "fail": data_fail},
              {"module": "中控", "total": orch, "pass": orch_pass, "fail": orch_fail},
              {"module": "工单", "total": order, "pass": order_pass, "fail": order_fail}
              ]

    print(f"count start——————————————————————{result}——————————————————————count end")
    return result


if __name__ == '__main__':
    r = [{'id': 'tests/test_page_load.py::test_for_page_performance[工单_建模器-/webapp/modeler-2000]', 'outcome': 'passed'}]
    c = CountResult()
    print(c.coe_pass)
    c.count_result(r)
    print(c.result)
    pass
