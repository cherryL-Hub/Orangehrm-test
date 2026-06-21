import requests

class Apiclient:
    def __init__(self,session):
        self.base_url = "https://opensource-demo.orangehrmlive.com/web/index.php"
        self.session=session

    def get_employee(self,empnumber):
        url=f"{self.base_url}/api/v2/pim/employees/{empnumber}"
        return self.session.get(url)

    def patch_employee(self,empnumber,data=None):
        url = f"{self.base_url}/api/v2/pim/employees/{empnumber}/personal-details"
        return self.session.put(url,data=data)

    def delete_employee(self, emp_number):
        url = f"{self.base_url}/api/v2/pim/employees"
        payload = {"ids": [emp_number]}
        return self.session.delete(url, json=payload)





