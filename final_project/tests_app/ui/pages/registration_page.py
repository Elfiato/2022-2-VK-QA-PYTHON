import allure

from ui.locators.basic_locators import RegistrationPageLocators
from ui.pages.base_page import BasePage
from utils.user_builder import UserBuilder
from app_urls import app_url


class RegistrationPage(BasePage):
    locators = RegistrationPageLocators()
    url = f'{app_url}/reg'

    @allure.step("Регистрация")
    def register(self, user_data):
        with allure.step(
                f'Регистрация пользователя с параметрами: имя: {user_data["name"][1]},\n'
                f'фамилия: {user_data["surname"][1]},\n'
                f'отчество: {user_data["middle_name"][1]},\n'
                f'имя пользователя: {user_data["username"][1]},\n'
                f'email: {user_data["email"][1]},\n'
                f'пароль: {user_data["password"][1]}.'):
            for key in user_data:
                self.input_text(*user_data[key][0], user_data[key][1])
            self.get_clickable_element(*self.locators.ACCEPT_CHECKBOX).click()
            self.get_clickable_element(*self.locators.SUBMIT_BUTTON).click()

    def get_user_data(self, invalid_arg=None, arg_len=None, valid_flag=True):
        user = UserBuilder()
        if valid_flag:
            user_data = user.get_valid_data()
        else:
            user_data = user.get_invalid_data(invalid_arg, arg_len)
        user_data = {
            'name': [self.locators.NAME_FIELD, user_data['name']],
            'surname': [self.locators.SURNAME_FIELD, user_data['surname']],
            'middle_name': [self.locators.NAME_FIELD, user_data['middle_name']],
            'username': [self.locators.USERNAME_FIELD, user_data['username']],
            'email': [self.locators.EMAIL_FIELD, user_data['email']],
            'password': [self.locators.PASSWORD_FIELD, user_data['password']],
            'confirm_password': [self.locators.CONFIRM_PASSWORD_FIELD, user_data['password']],
        }
        return user_data
