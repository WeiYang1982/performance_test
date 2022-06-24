import os

from src.utils.match_name import get_modules_name


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
    pass
