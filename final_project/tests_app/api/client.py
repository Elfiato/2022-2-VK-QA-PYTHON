import requests
from app_urls import app_url
import logging

logger = logging.getLogger('test')


class RespondErrorException(Exception):
    pass


class ApiClient:
    url = f'{app_url}/api'

    def __init__(self, base_url=None, session=None):
        if base_url is None:
            base_url = self.url
        self.url = base_url

        if session is None:
            session = requests.Session()
        self.session = session

    def login(self, username='test_username', password='test_password'):
        logger.info(f'Authorization via API and user - test_username.')
        location = f'{app_url}/login'

        data = {'username': username, 'password': password}
        return self._request(method='POST', location=location, data=data, allow_redirects=True)

    def _request(self, method, location, headers=None, data=None, params=None, allow_redirects=False, files=None,
                 jsonify=None, json=None):
        logger.info(f'Request with parameters: method:{method}, location:{location}, headers:{headers},'
                    f'data:{data}, params:{params}, allow_redirects:{allow_redirects}, jsonify:{jsonify}, json:{json}')
        if headers is None:
            headers = {
                'User-Agent': 'My User Agent 1.0'
            }
        else:
            headers['User-Agent'] = 'My User Agent 1.0'
        response = self.session.request(method=method, url=location, headers=headers, data=data, params=params,
                                        allow_redirects=allow_redirects, files=files, json=json)
        if jsonify:
            return response.json()
        return response
