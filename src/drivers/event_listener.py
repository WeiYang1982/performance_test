import traceback
import uuid

from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException, \
    StaleElementReferenceException, TimeoutException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.events import AbstractEventListener
from selenium.webdriver.support.wait import WebDriverWait

from src.utils.allure_logger import AllureLogger
from src.utils.high_light_element import HighLightElement
from src.utils.wait_for_element import WaitTime
import logging


class EventListener(AbstractEventListener):

    def __init__(self):
        logging.setLoggerClass(AllureLogger)
        # self.log = logging.getLogger(__name__)
        self.log = logging.getLogger(self.__class__.__module__)

    def before_click(self, element, driver):
        self.log.info("Will click the element %s" % element.get_attribute('class'))

    def before_find(self, by, value, driver):
        try:
            wait = WebDriverWait(driver,
                                 WaitTime.wait_for_element_timeout.value,
                                 WaitTime.wait_for_element_polling_during.value,
                                 ignored_exceptions=(ElementNotVisibleException,
                                                     StaleElementReferenceException,
                                                     TimeoutException))
            message = 'Element is not exists!'
            locator = (by, value)
            conditions = expected_conditions.presence_of_element_located(locator)
            wait.until(conditions, message)
        except TimeoutException as e:
            self.log.error("try to find element: %s %s, time out!" % (by, value))
            pass

    def before_navigate_to(self, url, driver):
        self.log.info("Before navigate to %s" % url)

    def before_change_value_of(self, element, driver):
        self.log.info("Element's value will be change from %s" % element.get_attribute("value"))

    def find_element(self, by='id', value=None):
        self.log.info("Find Element By: %s, Use Value: %s" % (by, value))

    def after_change_value_of(self, element, driver):
        self.log.info("Element's value change to %s" % element.get_attribute("value"))

    def after_click(self, element, driver):
        pass

    def after_find(self, by, value, driver):
        if by is not None:
            try:
                element = driver.find_element(by, value)
                driver.execute_script("arguments[0].scrollIntoView();", element)
                HighLightElement.high_light(driver, element)
            except NoSuchElementException:
                self.log.info("Element using: %s, value: %s, doesn't exist!" % (by, value))

    def after_navigate_to(self, url, driver):
        self.log.info("After navigate to %s" % url)

    def on_exception(self, exception, driver):
        type_name = exception.__class__.__name__
        self.log.error("There is a exception: %s, with messages: %s" % (type_name, traceback.format_exc()))
