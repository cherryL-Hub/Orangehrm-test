import allure
import pytest
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pytest import raises
from tests.conftest import driver
from tests.conftest import api_client_raw


@allure.feature("登录模块")
@allure.story("接口登录")
class TestLogin:

    @allure.title("测试登录接口 - 正确/错误密码")
    @allure.description("验证正确密码登录成功，错误密码返回 'Invalid credentials'")
    def test_api_login(self, api_client_raw):
        url = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/validate"
        session, token = api_client_raw

        password_test = {
            "admin345": False,
            "admin123": True,
        }

        for pwd, should_success in password_test.items():
            with allure.step(f"使用密码 '{pwd}' 尝试登录"):
                login_data = {
                    "_token": token,
                    "username": "Admin",
                    "password": pwd
                }
                response = session.post(url, data=login_data)

                if not should_success:
                    assert "Invalid credentials" in response.text
                    allure.attach(
                        response.text[:500],
                        name=f"错误响应（{pwd}）",
                        attachment_type=allure.attachment_type.TEXT
                    )
                    print("错误密码登录失败断言成功")
                else:
                    assert response.status_code == 200
                    print("登录成功，测试通过")