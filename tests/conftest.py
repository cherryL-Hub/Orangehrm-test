import time

import pytest
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from api_client_login import Apiclient

@pytest.fixture()
def api_client_raw():
    driver=webdriver.Chrome()
    driver.get("https://opensource-demo.orangehrmlive.com/")
    WebDriverWait(driver, 7).until(EC.visibility_of_element_located((By.NAME, "username")))
    token=driver.find_element(By.NAME,"_token").get_attribute("value")

    session=requests.Session()

    for cookie in driver.get_cookies():
        session.cookies.set(cookie['name'],cookie['value'])

    driver.quit()
    return session,token

@pytest.fixture()
def api_client(api_client_raw):
    base_url="https://opensource-demo.orangehrmlive.com/web/index.php/auth/validate"
    session,token=api_client_raw
    login_data={
         "_token":token,
         "username":"Admin",
         "password":"admin123"
     }

    response=session.post(base_url,data=login_data)

    assert response.status_code==200

    return Apiclient(session)




@pytest.fixture()
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()



@pytest.fixture()
def login_driver(driver):
    driver.get("https://opensource-demo.orangehrmlive.com/")
    time.sleep(10)

    username="Admin"
    password="admin123"

    driver.find_element(By.NAME,"username").send_keys(username)
    driver.find_element(By.NAME,"password").send_keys(password)
    driver.find_element(By.XPATH,"//button[@type='submit']").click()
    WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CLASS_NAME,"oxd-userdropdown-tab")))
    return driver


