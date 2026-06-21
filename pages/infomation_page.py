import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pytest import raises
import time
from tests.conftest import login_driver

class Infomation:
    def __init__(self,login_driver):
        self.infomation_driver=login_driver
        self.wait_card=(By.CLASS_NAME,"orangehrm-card-container")
        self.get_id_text = (By.XPATH, "//input[@class='oxd-input oxd-input--active']")
        self.back_list=(By.CLASS_NAME,"oxd-topbar-body-nav-tab-item")

    def card_wait(self):
        self.infomation_driver.find_element(*self.wait_card)

    def id_get(self):
        return self.infomation_driver.find_element(*self.get_id_text).text



    def click_list(self):
        self.infomation_driver.find_element(*self.back_list).click()
        from pages.pim_page import Pim
        return Pim(self.infomation_driver)