class HighLightElement:

    @staticmethod
    def high_light(webdriver, element):
        """
        高亮元素
        :param webdriver:
        :param element:
        :return:
        """
        webdriver.execute_script("arguments[0].style.border='3px solid red'", element)
        js = "var target = arguments[0];" + "setTimeout(function() { target.style.border='0'}, 2000)"
        webdriver.execute_script(js, element)
