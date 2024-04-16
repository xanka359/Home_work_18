import json

import allure
import requests
from selene import have, browser
from allure_commons.types import AttachmentType
from utils import load_schema
from jsonschema import validate
from tests.conftest import get_cookie


def add_item_into_basket_api_post(url, **kwargs):
    with allure.step("API Request"):
        result = requests.post(url="https://demowebshop.tricentis.com" + url, **kwargs)
        allure.attach(body=json.dumps(result.json(), indent=4, ensure_ascii=True),
                      name="Response", attachment_type=AttachmentType.JSON, extension="json")
    return result


def test_add_laptop_into_basket():
    cookie = get_cookie()

    with allure.step("open cataloge"):
        browser.open('')
        browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": cookie})
        browser.open('')

    with allure.step("add item into the basket"):
        url = "/addproducttocart/catalog/31/1/1"
        response = add_item_into_basket_api_post(url, cookies={"NOPCOMMERCE.AUTH": cookie})
        response_body = response.json()
        schema = load_schema("adding_item_into_basket.json")

        assert response.status_code == 200
        with open(schema) as file:
            schema = json.load(file)
            validate(response_body, schema=schema)

    with allure.step("Check existence items in the basket"):
        browser.driver.refresh()
        browser.element('.cart-label').with_(timeout=10).should(have.text('Shopping cart')).hover()
        #browser.config.timeout = 20
        browser.element('.mini-shopping-cart').element('.name').should(have.text('14.1-inch Laptop'))
        browser.element('.mini-shopping-cart').with_(timeout=10).element('[href="/cart"]').click()
        #browser.config.timeout = 10
        browser.element(".qty-input").set_value("0").press_enter()


def test_add_fiction_into_basket():
    cookie = get_cookie()

    with allure.step("open cataloge"):
        browser.open('')
        browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": cookie})
        browser.open('')

    with allure.step("add item into the basket"):
        url = "/addproducttocart/catalog/45/1/1"
        response = add_item_into_basket_api_post(url, cookies={"NOPCOMMERCE.AUTH": cookie})
        response_body = response.json()
        schema = load_schema("adding_item_into_basket.json")

        assert response.status_code == 200
        with open(schema) as file:
            schema = json.load(file)
            validate(response_body, schema=schema)

    with allure.step("Check existence items in the basket"):
        browser.driver.refresh()
        browser.element('.cart-label').with_(timeout=10).should(have.text('Shopping cart')).hover()
        #browser.config.timeout = 20
        browser.element('.mini-shopping-cart').element('.name').should(have.text('Fiction'))
        browser.element('.mini-shopping-cart').element('[href="/cart"]').click()
        #browser.config.timeout = 10
        browser.element(".qty-input").set_value("0").press_enter()
