import os

from dotenv import load_dotenv
from selene import browser
import pytest
import allure
import requests

load_dotenv()

LOGIN = os.getenv('LOGIN')
PASSWORD = os.getenv('PASSWORD')
URL = "https://demowebshop.tricentis.com"


def get_cookie():
    with allure.step("Login with API"):
        result = requests.post(
            url=URL + "/login",
            data={"Email": LOGIN, "Password": PASSWORD, "RememberMe": False},
            allow_redirects=False
        )

    with allure.step("Get cookie from API"):
        cookie = result.cookies.get("NOPCOMMERCE.AUTH")

    return cookie

@pytest.fixture(scope='function', autouse=True)
def manage_browser():
    browser.config.base_url = URL
    browser.config.window_height = 1080
    browser.config.window_width = 1920

    yield
    browser.quit()