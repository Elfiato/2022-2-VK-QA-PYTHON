import json
import random

import allure
from api.client import ApiClient
from app_urls import app_url
from utils.user_builder import UserBuilder


class ApiMain(ApiClient):
    url = f'{app_url}/api'

    def add_user(self, user_data):
        rel_url = '/user'
        location = self.url + rel_url
        headers = {
            'Content-Type': 'application/json'
        }
        with allure.step(f"Запрос к '{location}'c параметрами пользователя {user_data}."):
            data = {}
            for key, value in user_data.items():
                if key not in data and key != 'confirm_password' and key != 'middle_name':
                    data[key] = value
            data = json.dumps(data)
            res = self._request(method='POST', location=location, data=data, headers=headers)

        return res.status_code

    @staticmethod
    def get_user_data(invalid_arg=None, arg_len=None, valid_flag=True):
        user = UserBuilder()
        if valid_flag:
            return user.get_valid_data()
        return user.get_invalid_data(invalid_arg, arg_len)

    def delete_user(self, username):
        rel_url = f'/user/{username}'
        location = self.url + rel_url
        with allure.step(f"Удаление пользователя {username}"):
            res = self._request(method='DELETE', location=location)

        return res.status_code

    def update_password(self, username):
        new_password = str(random.randint(999999, 9999999))
        rel_url = f'/user/{username}/change-password'
        location = self.url + rel_url
        headers = {
            'Content-Type': 'application/json'
        }
        data = {
            "password": new_password
        }
        data = json.dumps(data)
        with allure.step(f"Обновление пароля пользователя {username}"):
            res = self._request(method='PUT', location=location, data=data, headers=headers)
        return res.status_code, new_password

    def change_user_status(self, username, status=False):
        rel_url = f'/user/{username}/block'
        if status:
            rel_url = f'/user/{username}/accept'
        location = self.url + rel_url
        with allure.step(f"Изменение статуса пользователя {username}"):
            res = self._request(method='POST', location=location)
        return res.status_code

    def get_app_status(self):
        rel_url = '/status'
        location = self.url + rel_url
        with allure.step(f"Получение статуса приложения."):
            res = self._request(method='GET', location=location)
        status_code = res.status_code
        res = res.json()

        return status_code, res
