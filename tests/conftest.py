from selene import browser
import pytest
import allure
import requests
from allure_commons.types import AttachmentType



LOGIN = "qaguru1@example.com"
PASSWORD = "123456"
URL = "https://demowebshop.tricentis.com"


def get_cookie():
    with allure.step("Login with API"):
        result = requests.post(
            url=URL + "/login",
            data={"Email": LOGIN, "Password": PASSWORD, "RememberMe": False},
            allow_redirects=False
        )
    #allure.attach(body=result.text, name="Response", attachment_type=AttachmentType.TEXT, extension="txt")
    #allure.attach(body=str(result.cookies), name="Cookies", attachment_type=AttachmentType.TEXT, extension="txt")
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