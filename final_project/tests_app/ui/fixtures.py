import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from ui.pages.main_page import MainPage
from ui.pages.registration_page import RegistrationPage
from ui.pages.welcome_page import WelcomePage


@pytest.fixture()
def driver(config, temp_dir):
    url = config['url']
    selenoid = config['selenoid']
    vnc = config['vnc']
    options = Options()
    options.add_experimental_option("prefs", {"download.default_directory": temp_dir})
    if selenoid:
        capabilities = {
            'browserName': 'chrome',
            "browserVersion": "108.0",
            "selenoid:options": {
                "enableVNC": True,
                "enableVideo": False
            }}
        if vnc:
            capabilities['enableVNC'] = True
        driver = webdriver.Remote(
            'http://127.0.0.1:4444/wd/hub',
            options=options,
            desired_capabilities=capabilities
        )
    else:
        if config['headless']:
            options.add_argument("--headless")
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),
                                  options=options)
    driver.get(url)
    driver.set_window_size(1920, 1080)
    yield driver
    driver.quit()


@pytest.fixture
def main_page(driver) -> MainPage:
    return MainPage(driver=driver)


@pytest.fixture
def registration_page(driver) -> RegistrationPage:
    return RegistrationPage(driver=driver)


@pytest.fixture
def welcome_page(driver) -> WelcomePage:
    return WelcomePage(driver=driver)
