import random

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pytest import raises
import time
from tests.conftest import login_driver

class Add:
    def __init__(self,login_driver):
        self.add_driver=login_driver
        self.firstName_send_wait=(By.NAME,"firstName")
        self.lastName_send=(By.NAME,"lastName")
        self.middleName_send=(By.NAME,"middleName")
        self.find_error = (By.XPATH, "//span[contains(@class, 'oxd-input-field-error-message')]")
        self.click_save=(By.XPATH,"//button[@class='oxd-button oxd-button--medium oxd-button--secondary orangehrm-left-space']")
        self.id_after_send=(By.XPATH,"//input[@class='oxd-input oxd-input--active oxd-input--error']")
    def wait_input(self):
        WebDriverWait(self.add_driver,10).until(EC.visibility_of_element_located(self.firstName_send_wait))
        return self

    def send_firstname(self,firstname):
        element=self.add_driver.find_element(*self.firstName_send_wait)
        element.send_keys(firstname)
        return self

    def send_middlename(self,middlename):
        element=self.add_driver.find_element(*self.middleName_send)
        element.send_keys(middlename)
        return self

    def send_lastname(self,lastname):
        element=self.add_driver.find_element(*self.lastName_send)
        element.send_keys(lastname)
        return self

    def error_find(self):
        WebDriverWait(self.add_driver, 2).until(
            EC.visibility_of_element_located(self.find_error)
        )
        return self.add_driver.find_element(*self.find_error).text

    def id_send(self):
        match=random.randint(1,99)
        self.add_driver.find_element(*self.id_after_send).send_keys(match)
        return self



    def save_click(self):
        self.add_driver.find_element(*self.click_save).click()
        from pages.infomation_page import Infomation
        return Infomation(self.add_driver)