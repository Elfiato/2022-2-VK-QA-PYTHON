import time
import logging
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotInteractableException, \
    InvalidElementStateException

logger = logging.getLogger('test')


class PageNotOpenedException(Exception):
    pass


class BasePage(object):
    WAITING_TIME = 10
    url = 'https://target-sandbox.my.com/'

    def __init__(self, driver):
        self.driver = driver
        logger.info(f'{self.__class__.__name__} page is opening...')

    def wait(self, timeout=None):
        if timeout is None:
            timeout = self.WAITING_TIME
        return WebDriverWait(self.driver, timeout=timeout)

    def get_present_element(self, how, what, timeout=None):
        logger.info(f'Getting element with locator: {how}: {what}.')
        return self.wait(timeout).until(EC.presence_of_element_located((how, what)))

    def get_clickable_element(self, how, what, timeout=None):
        logger.info(f'Getting element with locator: {how}: {what}.')
        return self.wait(timeout).until(EC.element_to_be_clickable((how, what)))

    def get_visible_element(self, how, what, timeout=None):
        logger.info(f'Getting element with locator: {how}: {what}.')
        return self.wait(timeout).until(EC.visibility_of_element_located((how, what)))

    def is_element_present(self, how, what, timeout=WAITING_TIME):
        logger.info(f'Checking is element present with locator: {how}: {what}.')
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((how, what)))
        except (NoSuchElementException, TimeoutException):
            return False
        return True

    def move_to_present_element(self, how, what):
        logger.info(f'Move to present element with locator: {how}: {what}.')
        action = ActionChains(self.driver)
        element = self.get_present_element(how, what)
        action.move_to_element(element).perform()

    def is_element_clickable(self, how, what, timeout=WAITING_TIME):
        logger.info(f'Checking is element clickable with locator: {how}: {what}.')
        try:
            WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable((how, what)))
        except (ElementNotInteractableException, InvalidElementStateException, TimeoutException):
            return False
        return True

    def is_opened(self, timeout=WAITING_TIME):
        logger.info(f'Checking page with url:{self.url} is opened.')
        started = time.time()
        while time.time() - started < timeout:
            if self.driver.current_url.startswith(self.url):
                return True
        raise PageNotOpenedException(f'{self.url} did not open in {timeout} sec, current url {self.driver.current_url}')

    def scroll_to_clickable_element(self, how, what):
        logger.info(f'Scrolling to element with locator: {how}: {what}.')
        element = self.get_clickable_element(how, what)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

    def open_page(self):
        logger.info(f'Opening page with url:{self.url}.')
        self.driver.get(self.url)
