import time
import re
import allure
import pytest
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from pytest import raises
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from tests.conftest import login_driver
from pages.dashboard_page import Dashboard
from pages.pim_page import Pim
from pages.add_page import Add
from pages.infomation_page import Infomation


def get_employee_id_from_url(login_driver):
    url = login_driver.current_url
    match = re.search(r'empNumber/(\d+)', url)
    if match:
        return match.group(1)
    return None


@allure.feature("员工管理模块")
@allure.story("UI 创建员工")
class TestPimUI:

    @allure.title("PIM 完整流程：UI 创建 → 接口查询 → 修改 → 删除")
    @allure.description(
        "覆盖：异常字段校验、ID冲突重试、员工创建、查询、修改、删除"
    )
    def test_pim_ui(self, login_driver, api_client):
        with allure.step("进入 PIM 页面"):
            dashboard_page = Dashboard(login_driver)
            pim_page = dashboard_page.pim_click()
            pim_page.pim_wait()

        employee_data = [
            ('', 2, 3),
            (3, 5, ''),
            (23, 5, 6)
        ]
        max_retries = 2
        employee_nubmer = None

        for f, m, l in employee_data:
            with allure.step(f"准备数据: firstname='{f}', middlename='{m}', lastname='{l}'"):
                add_page = pim_page.click_add()
                add_page.wait_input()
                add_page.send_firstname(f)
                add_page.send_middlename(m)
                add_page.send_lastname(l)

                retry_count = 0
                while retry_count < max_retries:
                    info_page = add_page.save_click()
                    time.sleep(2)

                    if "Employee Id already exists" in login_driver.page_source:
                        print("id已存在，新增数字")
                        add_page.id_send()
                        retry_count += 1
                        continue
                    break
                else:
                    print(f"数据 {f}，{m}，{l} 创建失败，进入下一组")
                    continue

                cs = None
                if f == '':
                    cs = "firstname"
                elif l == '':
                    cs = "lastname"

                if cs:
                    with allure.step(f"校验必填字段校验: {cs} 为空"):
                        text = add_page.error_find()
                        assert "Required" in text
                        print(f"预期无填写 {cs} 无效创建，测试成功")
                else:
                    with allure.step("创建成功，提取员工ID"):
                        info_page.card_wait()
                        time.sleep(10)
                        employee_nubmer = get_employee_id_from_url(login_driver)
                        print(employee_nubmer)
                        print("员工创建成功，测试通过")
                        break

        # ========== 接口删改查 ==========
        assert employee_nubmer is not None, "未成功创建任何员工"

        with allure.step(f"查询员工 ID={employee_nubmer}"):
            get_response = api_client.get_employee(employee_nubmer)
            assert get_response.status_code == 200
            em_id = get_response.json()["data"]["employeeId"]
            assert em_id is not None
            print(f"{em_id} 员工存在查询成功")

        with allure.step(f"修改员工 ID={employee_nubmer}"):
            patch_data = {
                "firstName": "jk",
                "middleName": "lk",
                "lastName": "ik"
            }
            patch_response = api_client.patch_employee(employee_nubmer, data=patch_data)
            assert patch_response.status_code == 200
            f_name = patch_response.json()["data"]["firstName"]
            assert f_name == patch_data["firstName"]
            print(f"员工信息修改成功，firstname: {f_name}")

        with allure.step(f"删除员工 ID={employee_nubmer}"):
            delete_response = api_client.delete_employee(employee_nubmer)
            print(f"删除状态码：{delete_response.status_code}")
            print(f"删除具体文本: {delete_response.text}")
            assert delete_response.status_code == 200

        with allure.step(f"验证员工 {employee_nubmer} 已不存在"):
            get_after_delete = api_client.get_employee(employee_nubmer)
            print(f"二次查询文本结果：{get_after_delete.text}")
            assert get_after_delete.status_code in [404, 422]
            print(f"{employee_nubmer} 不存在，删除成功")