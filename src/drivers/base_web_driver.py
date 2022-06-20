import os

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.support.event_firing_webdriver import EventFiringWebDriver
from webdriver_manager.chrome import ChromeDriverManager
from src.drivers.event_listener import EventListener


class BaseWebDriver:
    """
    webdriver基类
    """

    def __init__(self, executable_path=None, options=None, version=None):
        """
        打开浏览器
        :param executable_path: 支持本地路径，或者使用chromedrivermanager自动安装
        :param options: 默认使用最大化窗口
        :param version: 配合chromedrivermanager自动安装特定版本
        """
        d = DesiredCapabilities.CHROME
        d['loggingPrefs'] = {'performance': 'ALL'}
        registry_url = "https://registry.npmmirror.com/-/binary/chromedriver"
        if executable_path is None and version is None:
            executable_path = ChromeDriverManager(url=registry_url, latest_release_url=registry_url + "/LATEST_RELEASE").install()
        elif version is not None:
            executable_path = ChromeDriverManager(url=registry_url, latest_release_url=registry_url + "/LATEST_RELEASE", version=version).install()
        if options is None:
            options = webdriver.ChromeOptions()
            options.add_argument("--start-maximized")  # 最大化启动
            options.add_argument("disable-cache")  # 禁用缓存
            options.add_argument('--no-sandbox')  # 沙盒模式运行
            options.add_argument("–incognito")   # 无痕
            options.add_argument("disable-gpu")  # 禁用GPU加速
            options.add_argument("–disable-extensions")  # 禁用扩展
            options.add_argument("–no-first-run")  # 初始化时为空白页面
            options.add_argument('–disable-webgl')  # 禁用webgl
            options.add_argument('auto-open-devtools-for-tabs')  # 自动打开devtools
            options.add_argument('--disable-application-cache')
            options.add_argument("--disk-cache-size=0")
            options.add_argument("--disk-cache-dir=/dev/null")
            options.add_argument("--arc-disable-gms-core-cache")
            options.add_argument("--disable-back-forward-cache")
            options.add_argument("--disable-gpu-program-cache")
            options.add_argument("--disable-gpu-shader-disk-cache")
            # options.set_capability("goog:loggingPrefs", logPrefs)
            # options.add_experimental_option('w3c', False)
        # if os.environ['headless'] == 'True':
        #     options.add_argument('headless')
        driver_type = os.environ['driver_type']
        if driver_type == 'local':
            self.driver = webdriver.Chrome(desired_capabilities=d, executable_path=executable_path, options=options)
        if driver_type == 'remote':
            # options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
            # options.add_experimental_option("debuggerAddress", "172.25.128.26:9222")
            options.add_argument('auto-open-devtools-for-tabs')
            # self.driver = webdriver.Chrome(executable_path=executable_path, options=options)
            self.driver = webdriver.Remote(command_executor="http://172.25.128.26:4444/wd/hub", options=options)
            # web_driver = webdriver.Remote(command_executor="http://chrome:4444/wd/hub", options=chrome_options, )
        # self.driver.execute_cdp_cmd("Network.setCacheDisabled", {"cacheDisabled": True})
        # self.driver.execute_cdp_cmd("Performance.enable", {})
        self.driver = EventFiringWebDriver(self.driver, EventListener())
        self.driver.implicitly_wait(5)

    def get_driver(self):
        return self.driver


if __name__ == '__main__':

    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_experimental_option('debuggerAddress', '127.0.0.1:11111')
    # chrome_options.add_argument("--start-maximized")
    # web_driver = BaseWebDriver(options=chrome_options)
    web_driver = BaseWebDriver()
    try:
        web_driver.get_driver().get("http://www.baidu.com")
        for e in web_driver.get_driver().get_log('performance'):
            print(e)
    #     # web_driver.loop_find_element(web_driver.find_elements_by_id, 'kw')[0].send_keys("asdasd")
    #     # web_driver.find_element(By.ID, 'su').click()
    #     # web_driver.find_element(By.ID, 'ass')
    #     # from utils.capture_screenshot import ScreenShot
    #     # ScreenShot.take_screenshot(web_driver)
    # except Exception as e:
    #     raise e
    finally:
        web_driver.get_driver().quit()
        pass
