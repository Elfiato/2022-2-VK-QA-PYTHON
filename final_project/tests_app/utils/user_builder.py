import random

from faker import Faker
from ui.locators.basic_locators import RegistrationPageLocators


class UserBuilder:
    locators = RegistrationPageLocators()

    def __init__(self):
        fake = Faker()
        self.profile = fake.profile()
        self.password = fake.password()
        self.user_data = None

    def validate_password(self):
        password = [i for i in self.password]
        for i in range(len(password)):
            if password[i] in "!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}":
                password[i] = str(random.randint(0, 9))
        self.password = ''.join(password)

    def get_valid_data(self):
        self.validate_password()
        self.user_data = {
            'name': self.profile['name'].split()[0],
            'surname': self.profile['name'].split()[1],
            'middle_name': self.profile['name'].split()[0],
            'username': self.profile['username'][:16],
            'email': self.profile['mail'],
            'password': self.password,
            'confirm_password': self.password,
        }
        for key in self.user_data:
            if len(self.user_data[key]) < 6:
                self.user_data[key] *= 2
        return self.user_data

    def get_invalid_data(self, invalid_arg, arg_len):
        if self.user_data is None:
            self.get_valid_data()
        user_data = self.user_data.copy()
        if invalid_arg in self.user_data:
            user_data[invalid_arg] = 'a' * arg_len
            if invalid_arg == 'password':
                user_data['confirm_password'] = user_data[invalid_arg]
        else:
            raise KeyError(f"User data haven't {invalid_arg} key.")
        return user_data
