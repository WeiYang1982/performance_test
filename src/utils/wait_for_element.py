from enum import Enum
from selenium.common.exceptions import ElementNotVisibleException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.support.wait import WebDriverWait


class WaitTime(Enum):
    # 等待元素超时时间
    wait_for_element_timeout = 10
    # 轮询查找元素时间
    wait_for_element_polling_during = 0.1
    wait_for_element_when_page_loading = 5
    wait_for_element_loading_async_timeout = 30
    wait_for_element_dom_ready_timeout = 30


class WaitForElement:

    @staticmethod
    def wait_until(driver, conditions, message=''):
        """
        根据条件，动态等待元素
        忽略ElementNotVisibleException StaleElementReferenceException TimeoutException异常
        """
        wait = WebDriverWait(driver,
                             WaitTime.wait_for_element_timeout.value,
                             WaitTime.wait_for_element_polling_during.value,
                             ignored_exceptions=(ElementNotVisibleException,
                                                 StaleElementReferenceException,
                                                 TimeoutException))
        wait.until(conditions, message)

    @staticmethod
    def wait_until_not(driver, conditions, message=''):
        wait = WebDriverWait(driver,
                             WaitTime.wait_for_element_timeout.value,
                             WaitTime.wait_for_element_polling_during.value,
                             ignored_exceptions=(ElementNotVisibleException,
                                                 StaleElementReferenceException,
                                                 TimeoutException))
        wait.until_not(conditions, message)
