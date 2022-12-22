import allure

from ui.locators.basic_locators import WelcomePageLocators
from ui.pages.base_page import BasePage, PageNotOpenedException
from app_urls import app_url


class WelcomePage(BasePage):
    locators = WelcomePageLocators()
    url = f'{app_url}/welcome/'

    @allure.step("Проверка на наличе логина и имени пользователя в навбаре.")
    def is_user_data_in_navbar(self, name, lastname, username, middle_name=None):
        navbar_name, navbar_username = None, None
        if self.is_element_present(*self.locators.NAVBAR_NAME):
            navbar_name = self.get_present_element(*self.locators.NAVBAR_NAME).text.split(':')[-1].lstrip()
            navbar_name = navbar_name.split(' ')
        if self.is_element_present(*self.locators.NAVBAR_USERNAME):
            navbar_username = self.get_present_element(*self.locators.NAVBAR_USERNAME).text.split()[-1]
        if navbar_name and navbar_username:
            if len(navbar_name) == 2:
                return name == navbar_name[0] and lastname == navbar_name[1] and navbar_username == username
            return name == navbar_name[0] and lastname == navbar_name[1] and navbar_name[2] == middle_name \
                and navbar_username == username
        return False

    def is_welcome_page_opened(self):
        try:
            self.is_opened()
        except PageNotOpenedException:
            return False
        return True

    def is_new_window_opened(self):
        return self.get_amount_of_windows() > 1

    @allure.step("Нажатие на кнопку Home в навбаре.")
    def click_navbar_home_button(self):
        self.get_clickable_element(*self.locators.HOME_BUTTON).click()

    @allure.step("Нажатие на кнопку Python в навбаре.")
    def click_navbar_python_button(self):
        self.get_clickable_element(*self.locators.PYTHON_BUTTON).click()

    @allure.step("Нажатие на кнопку Python history в навбаре.")
    def click_navbar_python_history_button(self):
        self.move_to_present_element(*self.locators.PYTHON_BUTTON)
        self.get_clickable_element(*self.locators.PYTHON_HISTORY_BUTTON).click()

    @allure.step("Нажатие на кнопку About flask в навбаре.")
    def click_navbar_about_flask_button(self):
        self.move_to_present_element(*self.locators.PYTHON_BUTTON)
        self.get_clickable_element(*self.locators.ABOUT_FLASK_BUTTON).click()

    @allure.step("Нажатие на кнопку Download Centos в навбаре.")
    def click_navbar_download_centos_button(self):
        self.move_to_present_element(*self.locators.LINUX_BUTTON)
        self.get_clickable_element(*self.locators.DOWNLOAD_CENTOS_BUTTON).click()

    @allure.step("Нажатие на кнопку Wireshark news  в навбаре.")
    def click_navbar_wireshark_news_button(self):
        self.move_to_present_element(*self.locators.NETWORK_BUTTON)
        self.get_clickable_element(*self.locators.WIRESHARK_NEWS_BUTTON).click()

    @allure.step("Нажатие на кнопку Wireshark download в навбаре.")
    def click_navbar_wireshark_download_button(self):
        self.move_to_present_element(*self.locators.NETWORK_BUTTON)
        self.get_clickable_element(*self.locators.WIRESHARK_DOWNLOAD_BUTTON).click()

    @allure.step("Нажатие на кнопку TCP dump examples в навбаре.")
    def click_navbar_tcp_dump_examples_button(self):
        self.move_to_present_element(*self.locators.NETWORK_BUTTON)
        self.get_clickable_element(*self.locators.TCP_DUMP_EXAMPLES_BUTTON).click()

    @allure.step("Нажатие на кнопку What is an API.")
    def click_api_button(self):
        self.get_clickable_element(*self.locators.API_BUTTON).click()

    @allure.step("Нажатие на кнопку What is an API.")
    def click_future_of_internet_button(self):
        self.get_clickable_element(*self.locators.FUTURE_OF_INTERNET_BUTTON).click()

    @allure.step("Нажатие на кнопку What is an API.")
    def click_smtp_button(self):
        self.get_clickable_element(*self.locators.SMTP_BUTTON).click()

    @allure.step("Нажатие на кнопку logout.")
    def click_logout_button(self):
        self.get_clickable_element(*self.locators.LOGOUT_BUTTON).click()

    @allure.step('Сравнение VK_id полученного через апи и из навбара.')
    def is_vk_id_correct(self, vk_id, vk_id_navbar):
        return vk_id == vk_id_navbar

    @allure.step("Получение VK_id пользователя из навбара.")
    def is_vk_id_in_navbar(self):
        navbar_vk_id = None
        if self.is_element_present(*self.locators.VK_ID):
            navbar_vk_id_el = self.get_present_element(*self.locators.VK_ID).text.split(':')[-1].lstrip()
            navbar_vk_id = navbar_vk_id_el.split(' ')
        return str(navbar_vk_id[0])

    @allure.step("Получение фразы дзен python из футера.")
    def get_zen_of_python_footer_text(self):
        if self.is_element_present(*self.locators.FOOTER_TEXT):
            return self.get_present_element(*self.locators.FOOTER_TEXT).text
