import allure

from ui.locators.basic_locators import MainPageLocators
from ui.pages.base_page import BasePage
from ui.pages.registration_page import RegistrationPage
from ui.pages.welcome_page import WelcomePage


class MainPage(BasePage):
    locators = MainPageLocators()

    @allure.step("Открытие страницы регистрации.")
    def go_to_registration_page(self):
        registration_button = self.get_clickable_element(*self.locators.REGISTRATION_BUTTON)
        registration_button.click()
        return RegistrationPage(driver=self.driver)

    def log_in(self, username, password):
        with allure.step(f'Авторизация пользователя с данными: username - {username}, password - {password}.'):
            self.input_text(*self.locators.USERNAME_FIELD, username)
            self.input_text(*self.locators.PASSWORD_FIELD, password)
        self.get_clickable_element(*self.locators.SUBMIT_BUTTON).click()
        return WelcomePage(driver=self.driver)
