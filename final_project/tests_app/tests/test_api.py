import pytest
import allure

from api.api_main import ApiMain
from base import ApiBase


@pytest.mark.API
class TestApi(ApiBase):
    authorize = False

    @allure.title("Тест на добавление нового пользователя через API.")
    @allure.description("Добавление пользователя с валидными данными, полученными через Faker, "
                        "проверка статус кода ответа.")
    def test_add_user_status_code(self):
        api_main = ApiMain(session=self.api_client.session)
        user_data = api_main.get_user_data()
        status_code = api_main.add_user(user_data)
        assert status_code == 201, f'Статус код ответа равен {status_code}.'

    @pytest.mark.API_DB
    @allure.title("Тест на добавление нового пользователя через API DB.")
    @allure.description("Добавление пользователя с валидными данными, полученными через Faker, "
                        "проверка на наличе добавленного пользователя в базе данных.")
    def test_add_user_db(self):
        api_main = ApiMain(session=self.api_client.session)
        user_data = api_main.get_user_data()
        api_main.add_user(user_data)
        db_user_data = self.db_client.get_user_db(username=user_data['username'])
        assert db_user_data, 'Добавленного пользователя нет в базе данных.'
        compared_data = self.db_client.is_user_data_in_db(user_data, db_user_data[0])
        assert compared_data[0], f'Добавленная в базу данных информация не совпадает с отправленной: {compared_data[1]}'

    @allure.title("Тест на добавление нового пользователя с невалидными данными через API.")
    @allure.description("Добавление пользователя с невалидными данными, полученными через Faker, "
                        "проверка статус кода ответа.")
    @pytest.mark.parametrize('arg_len, invalid_arg, assert_text',
                             [(1, 'username', "длина логина 1 символ"),
                              (1, 'email', "длина почты 1 символ"),
                              (1, 'password', 'длина пароля 1 символ'),
                              (1000, 'name', 'длина имени 1000 символов'),
                              (1000, 'surname', 'длина фамилии 1000 символов'),
                              (1000, 'middle_name', 'длина отчества 1000 символов'),
                              (1000, 'password', 'длина пароля 1000 символов'),
                              ])
    def test_add_user_invalid_data_user_status_code(self, arg_len, invalid_arg, assert_text):
        with allure.step(f"Добавление пользователя с невалидными данными: {assert_text}."):
            api_main = ApiMain(session=self.api_client.session)
            user_data = api_main.get_user_data(valid_flag=False, invalid_arg=invalid_arg, arg_len=arg_len)
            status_code = api_main.add_user(user_data)
        assert status_code == 404, f'Статус код ответа равен {status_code}.'

    @pytest.mark.API_DB
    @allure.title("Тест на добавление нового пользователя с невалидными данными через API. DB.")
    @allure.description("Добавление пользователя с невалидными данными, полученными через Faker, "
                        "проверка на наличе добавленного пользователя в базе данных.")
    @pytest.mark.parametrize('arg_len, invalid_arg, assert_text',
                             [(1, 'username', "длина логина 1 символ"),
                              (1, 'email', "длина почты 1 символ"),
                              (1, 'password', 'длина пароля 1 символ'),
                              (1000, 'name', 'длина имени 1000 символов'),
                              (1000, 'surname', 'длина фамилии 1000 символов'),
                              (1000, 'middle_name', 'длина отчества 1000 символов'),
                              (1000, 'password', 'длина пароля 1000 символов'),
                              ])
    def test_add_invalid_data_user_db(self, arg_len, invalid_arg, assert_text):
        with allure.step(f"Добавление пользователя с невалидными данными: {assert_text}."):
            api_main = ApiMain(session=self.api_client.session)
            user_data = api_main.get_user_data(valid_flag=False, invalid_arg=invalid_arg, arg_len=arg_len)
            api_main.add_user(user_data)
        db_user_data = self.db_client.get_user_db(username=user_data['username'])
        assert not db_user_data, 'Пользователь с невалидными данными добавлен в базу данных.'

    @allure.title("Тест на удаление пользователя через API.")
    @allure.description("Удаление пользователя, проверка статус кода ответа.")
    def test_delete_user(self):
        api_main = ApiMain(session=self.api_client.session)
        user_data = api_main.get_user_data()
        self.db_client.add_user(user_data, 1)
        status_code = api_main.delete_user(user_data['username'])
        assert status_code == 204, f'Статус код ответа равен {status_code}.'

    @pytest.mark.API_DB
    @allure.title("Тест на удаление пользователя через API DB.")
    @allure.description("Удаление пользователя, проверка, что пользователя больше нет в базе.")
    def test_delete_user_db(self):
        api_main = ApiMain(session=self.api_client.session)
        user_data = api_main.get_user_data()
        self.db_client.add_user(user_data, 1)
        api_main.delete_user(user_data['username'])
        db_user_data = self.db_client.get_user_db(username=user_data['username'])
        assert not db_user_data, 'Удаленный пользователь есть в базе данных.'

    @allure.title("Тест на обновление пароля пользователя через API.")
    @allure.description("Обновление пароля пользователя и проверка статус кода ответа.")
    def test_update_password(self):
        api_main = ApiMain(session=self.api_client.session)
        user_data = api_main.get_user_data()
        self.db_client.add_user(user_data, 1)
        status_code = api_main.update_password(user_data['username'])[0]
        assert status_code == 200, f'Статус код ответа равен {status_code}.'

    @pytest.mark.API_DB
    @allure.title("Тест на обновление пароля пользователя через API DB.")
    @allure.description("Обновление пароля пользователя и проверка что пароль изменился в базе.")
    def test_update_password_db(self):
        api_main = ApiMain(session=self.api_client.session)
        user_data = api_main.get_user_data()
        self.db_client.add_user(user_data, 1)
        user_data['password'] = api_main.update_password(user_data['username'])[1]
        db_user_data = self.db_client.get_user_db(username=user_data['username'])
        assert db_user_data, 'Пользователя нет в базе данных.'
        compared_data = self.db_client.is_user_data_in_db(user_data, db_user_data[0])
        assert compared_data[0], f'Добавленная в базу данных информация не совпадает с отправленной: {compared_data[1]}'

    @pytest.mark.parametrize('start_status, status_flag', [(1, False), (0, True)])
    @allure.title("Тест на изменение статуса пользователя через API.")
    @allure.description("Тест на изменение статуса пользователя через API и проверка статус кода ответа.")
    def test_block_user(self, start_status, status_flag):
        api_main = ApiMain(session=self.api_client.session)
        user_data = api_main.get_user_data()
        self.db_client.add_user(user_data, start_status)
        status_code = api_main.change_user_status(user_data['username'], status_flag)
        assert status_code == 200, f'Статус код ответа равен {status_code}.'

    @pytest.mark.API_DB
    @pytest.mark.parametrize('start_status, status_flag', [(1, False), (0, True)])
    @allure.title("Тест на изменение статуса пользователя через API DB.")
    @allure.description("Тест на изменение статуса пользователя через API "
                        "что изменилось значения в столбце access базы данных.")
    def test_block_user_db(self, start_status, status_flag):
        api_main = ApiMain(session=self.api_client.session)
        user_data = api_main.get_user_data()
        self.db_client.add_user(user_data, start_status)
        api_main.change_user_status(user_data['username'], status_flag)
        db_user_data = self.db_client.get_user_db(username=user_data['username'])
        assert db_user_data, 'Пользователя нет в базе данных.'
        assert db_user_data[0].access == status_flag, "Значение поля access не было обновлено."

    @pytest.mark.API_DB
    @allure.title("Проверка статуса приложения.")
    @allure.description("Тест на получения статуса приложения, проверка содержимого и статус кода ответа.")
    def test_check_app_status_db(self):
        api_main = ApiMain(session=self.api_client.session)
        status_code, res = api_main.get_app_status()
        assert status_code == 200, f'Статус код ответа равен {status_code}.'
        assert res.get('status') == 'ok', f"Полученный ответ {res}."

    @pytest.mark.API_DB
    @pytest.mark.parametrize('status, res_status_code', [(0, 401), (1, 200)])
    @allure.title("Проверка возможности авторизации пользователя с измененным флагом доступа.")
    @allure.description("Тест на возможность авторизации пользователя через request "
                        "в зависимости от флага доступа access базы данных, проверка, "
                        "статус кода ответа главной страницы после авторизации.")
    def test_log_in_with_false_access_status(self, status, res_status_code):
        api_main = ApiMain(session=self.api_client.session)
        user_data = api_main.get_user_data()
        self.db_client.add_user(user_data, status)
        status_code = api_main.login(user_data['username'], user_data['password']).status_code
        assert status_code == res_status_code, f'Статус код ответа равен {status_code}.'
