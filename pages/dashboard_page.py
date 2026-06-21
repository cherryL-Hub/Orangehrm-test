import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pytest import raises
import time
from tests.conftest import login_driver

class Dashboard:
    def __init__(self,login_driver):
        self.dash_driver=login_driver
        self.click_pim=(By.XPATH,"//a[@href='/web/index.php/pim/viewPimModule']")

    def pim_click(self):
        self.dash_driver.find_element(*self.click_pim).click()
        from pages.pim_page import Pim
        return Pim(self.dash_driver)


