import sqlalchemy
from sqlalchemy.orm import sessionmaker

from db.models import User
import logging
import allure
from app_urls import db_host, db_port

logger = logging.getLogger('test')


class MySqlClient:

    def __init__(self, db_name, user, password):
        self.user = user
        self.port = db_port
        self.password = password
        self.host = db_host
        self.db_name = db_name

        self.connection = None
        self.engine = None
        self.session = None

    def connect(self, db_created=True):
        db = self.db_name if db_created else ''
        logger.info(f'Open db connection on {self.host}:{self.port}/{db} with usernmame - {self.user}.')
        url = f'mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{db}'
        self.engine = sqlalchemy.create_engine(url)
        self.connection = self.engine.connect()

        session = sessionmaker(bind=self.connection.engine)
        self.session = session()

    def execute_query(self, query, fetch=False):
        logger.info(f'Executing query {query}')
        res = self.connection.execute(query)
        if fetch:
            return res.fetchall()

    def get_db_results(self, **filters):
        logger.info(f'Getting db result with filters - {filters}')
        self.session.commit()
        result = self.session.query(User).filter_by(**filters).all()
        logger.info(f'Got db result - {result}')
        return result

    def get_user_db(self, username):
        with allure.step(f'Получение данных пользователя с логином - {username} из базы данных.'):
            return self.get_db_results(username=username)

    @staticmethod
    def is_user_data_in_db(user_data, db_user_data):
        diff_d = {'name': db_user_data.name,
                  'surname': db_user_data.surname,
                  'middle_name': db_user_data.middle_name,
                  'username': db_user_data.username,
                  'email': db_user_data.email,
                  'password': db_user_data.password}
        not_equal = []
        for key, val in diff_d.items():
            if user_data[key] != val:
                not_equal.append((user_data[key], val, key))
        not_equal = [f'{i[2]}: {i[0]} != {i[1]}' for i in not_equal]
        if not_equal:
            return False, ','.join(not_equal)
        return True, None

    def get_navbar_user_data(self, username):
        try:
            user_data = self.get_user_db(username)[0]
            return user_data.name, user_data.surname, user_data.active, user_data.middle_name
        except IndexError:
            return None

    def add_user(self, user_data, status):
        self.execute_query("INSERT INTO test_users(name, surname, middle_name, username, "
                           "password, email, access, active) "
                           "VALUES ('{0}', '{1}', '{2}', '{3}', "
                           "'{4}', '{5}', {6}, {7})".format(user_data['name'],
                                                            user_data['surname'],
                                                            user_data['middle_name'],
                                                            user_data['username'],
                                                            user_data['password'],
                                                            user_data['email'],
                                                            status,
                                                            0))
