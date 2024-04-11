import json

import allure
import requests
from selene import have, browser
from allure_commons.types import AttachmentType

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
        # response_body = response.json()
        # schema = load_schema("schema_adding_item_into_basket.json")

        assert response.status_code == 200
        # with open(schema) as file:
        #     schema = json.load(file)
        #     validate(response_body, schema=schema)


    with allure.step("Check quantity items in the basket"):
        browser.element('.cart-label').with_(timeout=10).should(have.text('Shopping cart')).hover()
        # browser.element('.mini-shopping-cart').element('.items').should(have.text('1 item(s)'))
        browser.element('.mini-shopping-cart').element('.name').should(have.text('14.1-inch Laptop'))
        # s('.mini-shopping-cart').element('.quantity').should.have.text('1')
        # browser.element('.mini-shopping-cart').element('.quantity').should(have.exact_text('Quantity: 1'))
