import importlib
from src.utils.change_type import change


def reflect_get_elements(webdriver, class_and_method_name, timestamp_name="null"):
    """
    反射的方法获取元素 需要文件名以及class名称一致(会自动以文件名转驼峰写法生成class名称)
    :param webdriver:
    :param class_and_method_name: 文件名(下划线写法) + 方法名，以.分割 如login_page.username
    :param timestamp_name: 文件参数，默认为null
    :return: 找到的元素
    """
    package = 'src.pages.'
    method_name = class_and_method_name.split(".")[-1]
    module_name = class_and_method_name.split(".")[-2]
    class_name = change(module_name)
    module = importlib.import_module(package + class_and_method_name.removesuffix("." + method_name))
    page = getattr(module, class_name)
    clasz = page(webdriver)
    method = getattr(clasz, method_name)
    if timestamp_name == "null":
        element = method
    else:
        element = method(name=timestamp_name)
    return element


def reflect_get_element(page_object, element_name):
    method = getattr(page_object, element_name)
    return method()


if __name__ == '__main__':
    name = 'data_framework.login_page.login_url'

    # reflect_get_elements(webdriver=None, class_and_method_name=name)
    str = '0123456789'
    print(name[:-1])