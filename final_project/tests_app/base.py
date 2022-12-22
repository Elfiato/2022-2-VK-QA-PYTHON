import os

import allure
import pytest
from _pytest.fixtures import FixtureRequest
from db.client import MySqlClient
from requests import request
from app_urls import vk_id_url


class BaseCase:
    driver = None

    @pytest.fixture(scope='function', autouse=True)
    def ui_report(self, driver, request, temp_dir):
        failed_test_count = request.session.testsfailed
        yield
        if request.session.testsfailed > failed_test_count:
            browser_logs = os.path.join(temp_dir, 'browser.log')
            test_log = os.path.join(temp_dir, 'test.log')
            with open(browser_logs, 'w') as f:
                for i in driver.get_log('browser'):
                    f.write(f"{i['level']} - {i['source']}\n{i['message']}\n")
            screenshot_path = os.path.join(temp_dir, 'failed.png')
            self.driver.save_screenshot(filename=screenshot_path)
            allure.attach.file(screenshot_path, 'failed.png', allure.attachment_type.PNG)
            with open(browser_logs, 'r') as f:
                allure.attach(f.read(), 'browser.log', allure.attachment_type.TEXT)
            with open(test_log, 'r') as f:
                allure.attach(f.read(), 'test.log', allure.attachment_type.TEXT)

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config, logger, request: FixtureRequest, mysql_client):
        self.driver = driver
        self.config = config
        self.logger = logger
        self.db_client: MySqlClient = mysql_client

    @allure.step("Получение VK_id пользователя.")
    def get_vk_id_with_requests(self, username):
        location = f'{vk_id_url}/vk_id/{username}'
        response = request(method='GET', url=location)
        if response.status_code == 200:
            return str(response.json()['vk_id'])
        assert False, "Сервис vk_id недоступен."


class BaseCaseLogIn(BaseCase):
    authorize = True

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config, request: FixtureRequest, logger, mysql_client, api_client):
        self.driver = driver
        self.config = config
        self.logger = logger
        self.db_client: MySqlClient = mysql_client
        self.api_client = api_client

        if not self.authorize:
            self.api_client.login()
            cookies = self.api_client.session.cookies.get_dict()
            for cookie_name, cookie_value in cookies.items():
                self.driver.add_cookie({'name': cookie_name, 'value': cookie_value})

            self.driver.refresh()


class ApiBase:
    authorize = True

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, api_client, mysql_client, logger, config):
        self.api_client = api_client
        self.db_client: MySqlClient = mysql_client
        self.logger = logger
        self.config = config

        if not self.authorize:
            self.api_client.login()
