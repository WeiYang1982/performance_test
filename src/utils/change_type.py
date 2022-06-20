def change(string):
    """
    下划线写法转驼峰写法
    :param string:
    :return:
    """
    if "_" in string:
        return "".join(map(lambda x: x.capitalize(), string.split("_")))
