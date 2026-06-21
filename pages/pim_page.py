import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pytest import raises
import time
from tests.conftest import login_driver

class Pim:
    def __init__(self,login_driver):
        self.pim_driver=login_driver
        self.wait_click_pim = (By.XPATH, "//a[text()='Add Employee']")


    def pim_wait(self):
        WebDriverWait(self.pim_driver,5).until(EC.element_to_be_clickable(self.wait_click_pim))
        return self

    def click_add(self):
        self.pim_driver.find_element(*self.wait_click_pim).click()
        from pages.add_page import Add
        return Add(self.pim_driver)

