from selenium.webdriver.common.by import By


class MainPageLocators:
    REGISTRATION_BUTTON = (By.CSS_SELECTOR, ".uk-text-small a")
    USERNAME_FIELD = (By.CSS_SELECTOR, "#username")
    PASSWORD_FIELD = (By.CSS_SELECTOR, "#password")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, '#submit')


class RegistrationPageLocators:
    NAME_FIELD = (By.CSS_SELECTOR, "#user_name")
    SURNAME_FIELD = (By.CSS_SELECTOR, "#user_surname")
    MIDDLE_NAME_FIELD = (By.CSS_SELECTOR, "#user_middle_name")
    USERNAME_FIELD = (By.CSS_SELECTOR, "#username")
    EMAIL_FIELD = (By.CSS_SELECTOR, "#email")
    PASSWORD_FIELD = (By.CSS_SELECTOR, "#password")
    CONFIRM_PASSWORD_FIELD = (By.CSS_SELECTOR, "#confirm")
    ACCEPT_CHECKBOX = (By.CSS_SELECTOR, '#term')
    SUBMIT_BUTTON = (By.CSS_SELECTOR, '#submit')


class WelcomePageLocators:
    NAVBAR_NAME = (By.CSS_SELECTOR, "#login-name li:nth-child(2)")
    NAVBAR_USERNAME = (By.CSS_SELECTOR, '#login-name li:nth-child(1)')
    VK_ID = (By.CSS_SELECTOR, '#login-name li:nth-child(3)')
    HOME_BUTTON = (By.CSS_SELECTOR, ".uk-navbar-nav>li:nth-child(2)>a")
    PYTHON_BUTTON = (By.CSS_SELECTOR, ".uk-navbar-nav>li:nth-child(3)>a")
    LINUX_BUTTON = (By.CSS_SELECTOR, ".uk-navbar-nav>li:nth-child(4)>a")
    NETWORK_BUTTON = (By.CSS_SELECTOR, ".uk-navbar-nav>li:nth-child(5)>a")
    PYTHON_HISTORY_BUTTON = (By.CSS_SELECTOR, ".uk-navbar-nav>li:nth-child(3) li:nth-child(1) a")
    ABOUT_FLASK_BUTTON = (By.CSS_SELECTOR, ".uk-navbar-nav>li:nth-child(3) li:nth-child(2) a")
    DOWNLOAD_CENTOS_BUTTON = (By.CSS_SELECTOR, ".uk-navbar-nav>li:nth-child(4) li:nth-child(1) a")
    WIRESHARK_NEWS_BUTTON = (By.CSS_SELECTOR, ".uk-nav-sub>li:nth-child(1) a")
    WIRESHARK_DOWNLOAD_BUTTON = (By.CSS_SELECTOR, ".uk-nav-sub>li:nth-child(2) a")
    TCP_DUMP_EXAMPLES_BUTTON = (By.CSS_SELECTOR, ".uk-nav-header:nth-child(2) a")
    LOGOUT_BUTTON = (By.CSS_SELECTOR, "#logout a")
    API_BUTTON = (By.CSS_SELECTOR, ".uk-text-center:nth-child(1) .uk-overlay")
    FUTURE_OF_INTERNET_BUTTON = (By.CSS_SELECTOR, ".uk-text-center:nth-child(2) .uk-overlay")
    SMTP_BUTTON = (By.CSS_SELECTOR, ".uk-text-center:nth-child(3) .uk-overlay")
    FOOTER_TEXT = (By.CSS_SELECTOR, "footer p:first-child")
