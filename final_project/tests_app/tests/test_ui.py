import allure
import pytest

from _pytest.fixtures import FixtureRequest

from base import BaseCase, BaseCaseLogIn
from app_urls import app_url


@pytest.mark.UI
@pytest.mark.UI_registration
class TestUIRegistration(BaseCase):
    @allure.title("Позитивный тест формы регистрации пользователя UI.")
    @allure.description("Регистрация пользователя с валидными данными, проверка, что после регистрации произведен "
                        "переход на главную страницу и в навбаре есть имя и логин пользователя.")
    def test_registration_with_valid_data(self, request: FixtureRequest):
        with allure.step("Открытие страницы авторизации."):
            main_page = request.getfixturevalue('main_page')
            main_page.is_opened()
        registration_page = main_page.go_to_registration_page()
        registration_page.is_opened()
        user_data = registration_page.get_user_data(valid_flag=True)
        registration_page.register(user_data)
        welcome_page = request.getfixturevalue('welcome_page')
        welcome_page.is_opened()
        assert welcome_page.is_user_data_in_navbar(user_data['name'][1], user_data['surname'][1],
                                                   user_data['username'][1]), \
            "После регистрации на главной странице в навбаре не отражены данные пользователя."

    @pytest.mark.UI_DB
    @allure.title("Позитивный тест формы регистрации пользователя DB.")
    @allure.description("Регистрация пользователя с валидными данными, "
                        "проверка что данные добавленные в базу совпадают с введенными.")
    def test_registration_with_valid_data_db(self, request: FixtureRequest):
        with allure.step("Открытие страницы авторизации."):
            main_page = request.getfixturevalue('main_page')
            main_page.is_opened()
        registration_page = main_page.go_to_registration_page()
        registration_page.is_opened()
        user_data = registration_page.get_user_data(valid_flag=True)
        registration_page.register(user_data)
        welcome_page = request.getfixturevalue('welcome_page')
        welcome_page.is_opened()
        db_user_data = self.db_client.get_user_db(username=user_data['username'][1])
        assert db_user_data, 'Зарегистрированного пользователя нет в базе данных.'
        compared_data = self.db_client.is_user_data_in_db(user_data, db_user_data[0])
        assert compared_data[0], f'Добавленная в базу данных информация не совпадает с отправленной: {compared_data[1]}'

    @pytest.mark.UI_DB
    @allure.title("Негативный тест формы регистрации пользователя DB.")
    @allure.description("Регистрация пользователя с невалидными данными.")
    @pytest.mark.parametrize('arg_len, invalid_arg, assert_text',
                             [(1, 'username', "длина логина 1 символ"),
                              (1, 'email', "длина почты 1 символ"),
                              (1, 'password', 'длина пароля 1 символ'),
                              (1000, 'name', 'длина имени 1000 символов'),
                              (1000, 'surname', 'длина фамилии 1000 символов'),
                              (1000, 'middle_name', 'длина отчества 1000 символов'),
                              (1000, 'password', 'длина пароля 1000 символов'),
                              ])
    def test_registration_with_invalid_data(self, request: FixtureRequest, arg_len, assert_text, invalid_arg):
        with allure.step("Открытие страницы авторизации."):
            main_page = request.getfixturevalue('main_page')
            main_page.is_opened()
        registration_page = main_page.go_to_registration_page()
        registration_page.is_opened()
        user_data = registration_page.get_user_data(valid_flag=False, invalid_arg=invalid_arg, arg_len=arg_len)
        registration_page.register(user_data)
        db_user_data = self.db_client.get_user_db(username=user_data['username'][1])
        assert not db_user_data, f'Произошла регистрация пользователя (данные пользователя добавлены в базу) ' \
                                 f'с невалидными данными: {assert_text}.'


@pytest.mark.UI
@pytest.mark.UI_authorization
class TestUIAuthorization(BaseCase):
    @pytest.mark.UI_DB
    @allure.title("Позитивный тест авторизации пользователя.")
    @allure.description("Авторизация пользователя, добавленного в базу при поднятии контейнера, "
                        "проверка, что произведен переход на главную страницу "
                        "и в навбаре отображаются данные пользователя.")
    def test_log_in_with_valid_data(self, request: FixtureRequest):
        username = 'test_username'
        password = 'test_password'
        with allure.step("Открытие страницы авторизации."):
            main_page = request.getfixturevalue('main_page')
            main_page.is_opened()
        welcome_page = main_page.log_in(username, password)
        welcome_page.is_welcome_page_opened()
        db_navbar_user_data = self.db_client.get_navbar_user_data(username)
        assert welcome_page.is_user_data_in_navbar(db_navbar_user_data[0], db_navbar_user_data[1],
                                                   username, middle_name=db_navbar_user_data[-1]), \
            "После авторизации на главной странице в навбаре не отражены данные пользователя."
        with allure.step("Проверка на изменение статуса пользователя в базе."):
            assert db_navbar_user_data[2] == 1, 'Статус авторизованного пользователя в базе не равен 1.'

    @pytest.mark.UI_DB
    @allure.title("Позитивный тест авторизации пользователя DB.")
    @allure.description("Авторизация пользователя, добавленного в базу при поднятии контейнера, "
                        "проверка, что статус пользователя в базе изменился.")
    def test_log_in_with_valid_data_db(self, request: FixtureRequest):
        username = 'test_username'
        password = 'test_password'
        with allure.step("Открытие страницы авторизации."):
            main_page = request.getfixturevalue('main_page')
            main_page.is_opened()
        welcome_page = main_page.log_in(username, password)
        welcome_page.is_welcome_page_opened()
        db_navbar_user_data = self.db_client.get_navbar_user_data(username)
        with allure.step("Проверка на изменение статуса пользователя в базе."):
            assert db_navbar_user_data[2] == 1, 'Статус авторизованного пользователя в базе не равен 1.'

    @pytest.mark.UI_DB
    @allure.title("Негативный тест авторизации пользователя.")
    @allure.description("Авторизация пользователя, с невалидными данными.")
    @pytest.mark.parametrize('username, password, assert_text', [
        ('test_username', 'asdf', 'Верный логин, неверный пароль.'),
        ('asdfasdf234', 'test_password', 'Неверный логин, верный пароль.'),
        ('asdfasdf234', 'asdf', 'Неверный логин, неверный пароль.')])
    def test_log_in_with_invalid_data(self, request: FixtureRequest, username, password, assert_text):
        with allure.step("Открытие страницы авторизации."):
            main_page = request.getfixturevalue('main_page')
            main_page.is_opened()
        welcome_page = main_page.log_in(username, password)
        welcome_page.is_welcome_page_opened()
        db_navbar_user_data = self.db_client.get_navbar_user_data(username)
        if db_navbar_user_data:
            assert not welcome_page.is_user_data_in_navbar(db_navbar_user_data[0], db_navbar_user_data[1],
                                                           username, middle_name=db_navbar_user_data[-1]), \
                f"Произошла авторизация с невалидными данными: username - {username}, password - {password}."
            with allure.step("Проверка на изменение статуса пользователя в базе."):
                assert not db_navbar_user_data[2] == 0, 'Статус неавторизованного пользователя в базе не равен 0.'
        else:
            assert True, 'Незарегистрированный пользователь есть в базе данных.'


@pytest.mark.UI
@pytest.mark.UI_velcome_page
class TestUIWelcomePage(BaseCaseLogIn):
    authorize = False

    @allure.title("Тест кнопки Home в навбаре.")
    @allure.description("Нажатие кнопки Home и проверка, что произведен переход на главную страницу.")
    def test_navbar_home_button(self, request: FixtureRequest):
        with allure.step("Открытие главной страницы."):
            welcome_page = request.getfixturevalue('welcome_page')
            welcome_page.is_opened()
        welcome_page.click_navbar_home_button()
        assert welcome_page.is_welcome_page_opened(), \
            'После нажатия кнопки Home в навбаре не перешел переход на главную страницу.'

    @allure.title("Тест кнопки Python в навбаре.")
    @allure.description("Нажатие кнопки Python и проверка, что открыта новая вкладка с требуемым адресом.")
    def test_navbar_python_button(self, request: FixtureRequest):
        url = 'https://www.python.org/'
        with allure.step("Открытие главной страницы."):
            welcome_page = request.getfixturevalue('welcome_page')
            welcome_page.is_opened()
        welcome_page.click_navbar_python_button()
        assert welcome_page.is_new_window_opened(), 'После нажатия кнопки Python в навбаре,' \
                                                    ' не открылось новой вкладки.'
        welcome_page.switch_to_next_window()
        assert welcome_page.check_current_url(url), f'Адрес новой вкладки не соответствует адресу {url}.'

    @allure.title("Тест кнопки Python history в навбаре.")
    @allure.description("Нажатие кнопки Python history и проверка, что открыта новая вкладка с требуемым адресом.")
    def test_navbar_python_history_button(self, request: FixtureRequest):
        url = 'https://en.wikipedia.org/wiki/History_of_Python'
        with allure.step("Открытие главной страницы."):
            welcome_page = request.getfixturevalue('welcome_page')
            welcome_page.is_opened()
        welcome_page.click_navbar_python_history_button()
        assert welcome_page.is_new_window_opened(), 'После нажатия кнопки Python history в навбаре,' \
                                                    ' не открылось новой вкладки.'
        welcome_page.switch_to_next_window()
        assert welcome_page.check_current_url(url), f'Адрес новой вкладки не соответствует адресу {url}.'

    @allure.title("Тест кнопки About flask в навбаре.")
    @allure.description("Нажатие кнопки About flask и проверка, что открыта новая вкладка с требуемым адресом.")
    def test_navbar_about_flask_button(self, request: FixtureRequest):
        url = 'https://flask.palletsprojects.com/en/1.1.x/#'
        with allure.step("Открытие главной страницы."):
            welcome_page = request.getfixturevalue('welcome_page')
            welcome_page.is_opened()
        welcome_page.click_navbar_about_flask_button()
        assert welcome_page.is_new_window_opened(), 'После нажатия кнопки About flask в навбаре,' \
                                                    ' не открылось новой вкладки.'
        welcome_page.switch_to_next_window()
        assert welcome_page.check_current_url(url), f'Адрес новой вкладки не соответствует адресу {url}.'

    @allure.title("Тест кнопки Download Centos в навбаре.")
    @allure.description("Нажатие кнопки Download Centos и проверка, что открыта новая вкладка с требуемым адресом.")
    def test_navbar_download_centos_button(self, request: FixtureRequest):
        url = 'https://www.centos.org/download/'
        with allure.step("Открытие главной страницы."):
            welcome_page = request.getfixturevalue('welcome_page')
            welcome_page.is_opened()
        welcome_page.click_navbar_download_centos_button()
        assert welcome_page.is_new_window_opened(), 'После нажатия кнопки Download Centos в навбаре,' \
                                                    ' не открылось новой вкладки.'
        welcome_page.switch_to_next_window()
        assert welcome_page.check_current_url(url), f'Адрес новой вкладки не соответствует адресу {url}.'

    @allure.title("Тест кнопки Wireshark news в навбаре.")
    @allure.description("Нажатие кнопки Wireshark news и проверка, что открыта новая вкладка с требуемым адресом.")
    def test_navbar_wireshark_news_button(self, request: FixtureRequest):
        url = 'https://www.wireshark.org/news/'
        with allure.step("Открытие главной страницы."):
            welcome_page = request.getfixturevalue('welcome_page')
            welcome_page.is_opened()
        welcome_page.click_navbar_wireshark_news_button()
        assert welcome_page.is_new_window_opened(), 'После нажатия кнопки Wireshark news в навбаре,' \
                                                    ' не открылось новой вкладки.'
        welcome_page.switch_to_next_window()
        assert welcome_page.check_current_url(url), f'Адрес новой вкладки не соответствует адресу {url}.'

    @allure.title("Тест кнопки Wireshark download в навбаре.")
    @allure.description("Нажатие кнопки Wireshark download и проверка, что открыта новая вкладка с требуемым адресом.")
    def test_navbar_wireshark_download_button(self, request: FixtureRequest):
        url = 'https://www.wireshark.org/#download'
        with allure.step("Открытие главной страницы."):
            welcome_page = request.getfixturevalue('welcome_page')
            welcome_page.is_opened()
        welcome_page.click_navbar_wireshark_download_button()
        assert welcome_page.is_new_window_opened(), 'После нажатия кнопки Wireshark download в навбаре,' \
                                                    ' не открылось новой вкладки.'
        welcome_page.switch_to_next_window()
        assert welcome_page.check_current_url(url), f'Адрес новой вкладки не соответствует адресу {url}.'

    @allure.title("Тест кнопки TCP dump examples в навбаре.")
    @allure.description("Нажатие кнопки TCP dump examples и проверка, что открыта новая вкладка с требуемым адресом.")
    def test_navbar_tcp_dump_examples_button(self, request: FixtureRequest):
        url = 'https://hackertarget.com/tcpdump-examples/'
        with allure.step("Открытие главной страницы."):
            welcome_page = request.getfixturevalue('welcome_page')
            welcome_page.is_opened()
        welcome_page.click_navbar_tcp_dump_examples_button()
        assert welcome_page.is_new_window_opened(), 'После нажатия кнопки TCP dump examples в навбаре,' \
                                                    ' не открылось новой вкладки.'
        welcome_page.switch_to_next_window()
        assert welcome_page.check_current_url(url), f'Адрес новой вкладки не соответствует адресу {url}.'

    @allure.title("Тест кнопки What is an API.")
    @allure.description("Нажатие кнопки What is an API и проверка, что открыта новая вкладка с требуемым адресом.")
    def test_api_button(self, request: FixtureRequest):
        url = 'https://en.wikipedia.org/wiki/API'
        with allure.step("Открытие главной страницы."):
            welcome_page = request.getfixturevalue('welcome_page')
            welcome_page.is_opened()
        welcome_page.click_api_button()
        assert welcome_page.is_new_window_opened(), 'После нажатия кнопки What is an API' \
                                                    ' не открылось новой вкладки.'
        welcome_page.switch_to_next_window()
        assert welcome_page.check_current_url(url), f'Адрес новой вкладки не соответствует адресу {url}.'

    @allure.title("Тест кнопки Future of internet.")
    @allure.description("Нажатие кнопки Future of internet и проверка, что открыта новая вкладка с требуемым адресом.")
    def test_future_of_internet_button(self, request: FixtureRequest):
        url = 'https://www.popularmechanics.com/technology/infrastructure/a29666802/future-of-the-internet/'
        with allure.step("Открытие главной страницы."):
            welcome_page = request.getfixturevalue('welcome_page')
            welcome_page.is_opened()
        welcome_page.click_future_of_internet_button()
        assert welcome_page.is_new_window_opened(), 'После нажатия кнопки Future of internet' \
                                                    ' не открылось новой вкладки.'
        welcome_page.switch_to_next_window()
        assert welcome_page.check_current_url(url), f'Адрес новой вкладки не соответствует адресу {url}.'

    @allure.title("Тест кнопки Lets talk about SMTP.")
    @allure.description(
        "Нажатие кнопки Lets talk about SMTP и проверка, что открыта новая вкладка с требуемым адресом.")
    def test_smptp_button(self, request: FixtureRequest):
        url = 'https://ru.wikipedia.org/wiki/SMTP'
        with allure.step("Открытие главной страницы."):
            welcome_page = request.getfixturevalue('welcome_page')
            welcome_page.is_opened()
        welcome_page.click_smtp_button()
        assert welcome_page.is_new_window_opened(), 'После нажатия кнопки Lets talk about SMTP' \
                                                    ' не открылось новой вкладки.'
        welcome_page.switch_to_next_window()
        assert welcome_page.check_current_url(url), f'Адрес новой вкладки не соответствует адресу {url}.'

    @allure.title("Тест кнопки logout.")
    @allure.description(
        "Нажатие кнопки logout и проверка, что произведен выход из системы.")
    def test_logout_button(self, request: FixtureRequest):
        url = f'{app_url}/login'
        with allure.step("Открытие главной страницы."):
            welcome_page = request.getfixturevalue('welcome_page')
            welcome_page.is_opened()
        welcome_page.click_logout_button()
        assert welcome_page.check_current_url(url), f'После нажатия кнопки logout не произошло выхода из системы.'

    @allure.title("Тест отображения VK_ID в навбаре.")
    @allure.description(
        "Получение VK_ID пользователя через requests, и проверка, что он отображен в навбаре.")
    def test_vk_id_button(self, request: FixtureRequest):
        with allure.step("Открытие главной страницы."):
            welcome_page = request.getfixturevalue('welcome_page')
            welcome_page.is_opened()
        vk_id = self.get_vk_id_with_requests('test_username')
        vk_id_navbar = welcome_page.is_vk_id_in_navbar()
        assert welcome_page.is_vk_id_correct(vk_id, vk_id_navbar), f' VK_ID, полученный от VK_ID_API ' \
                                                                   f'не равен полученному ' \
                                                                   f'из навбара: {vk_id} != {vk_id_navbar}'

    @allure.title("Тест отображения дзен python в футере.")
    @allure.description(
        "Получение фразы дзен python из футера, обновление страницы, "
        "снова получение фразы, проверка, что фразы не совпадают.")
    def test_zen_of_python_button(self, request: FixtureRequest):
        with allure.step("Открытие главной страницы."):
            welcome_page = request.getfixturevalue('welcome_page')
            welcome_page.is_opened()
        zen_of_python_phrase_first = welcome_page.get_zen_of_python_footer_text()
        welcome_page.refresh()
        zen_of_python_phrase_second = welcome_page.get_zen_of_python_footer_text()
        assert zen_of_python_phrase_first != zen_of_python_phrase_second, f'Фраза дзен python получаемая при ' \
                                                                          f'обновлении страницы появилась ' \
                                                                          f'два раза подряд.'
