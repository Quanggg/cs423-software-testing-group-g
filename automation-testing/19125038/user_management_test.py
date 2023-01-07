# SELENIUM
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# UNITTEST
import unittest

# DATA
from ddt import ddt, data, unpack

# CONSTANT
from constant import WEB_BASE_URL

# UTILS
from utils import get_csv_data


@ddt
class TestUserManagement(unittest.TestCase):
    def setUp(self):
        options = Options()
        options._proxy = None
        options.add_experimental_option('detach', True)
        self.driver = webdriver.Chrome(options=options)
        # self.driver = webdriver.Safari(options=options)
        # self.driver = webdriver.Firefox(options=options)
        self.driver.implicitly_wait(5)
        self.driver.get(WEB_BASE_URL)

        self.login()

    def tearDown(self):
        self.driver.quit()

    def login(self):
        username_element = self.driver.find_element(By.NAME, 'username')
        password_element = self.driver.find_element(By.NAME, 'password')
        username_element.send_keys('Admin')
        password_element.send_keys('admin123')
        login_button_element = self.driver.find_element(
            By.CSS_SELECTOR, 'button[class*="orangehrm-login-button"]')
        login_button_element.click()

    def goToUserManagement(self):
        admin_element = self.driver.find_element(
            By.CSS_SELECTOR, 'a[href*="/web/index.php/admin/viewAdminModule"]')
        admin_element.click()

    @data(*get_csv_data("user_management_data.csv"))
    @unpack
    def test_user_management(self, username='', user_role='Select', employee_name='', status='Select', result='100'):
        try:
            self.goToUserManagement()

            input_fields = {
                "Username": username,
                "Employee Name": employee_name,
            }

            dropdown_fields = {
                "User Role": user_role,
                "Status": status
            }

            # Fill in input_fields
            for field, value in input_fields.items():
                tempElement = list(filter(
                    lambda x: x.find_element(
                        By.CSS_SELECTOR,
                        'label[class*="oxd-label"]'
                    ).text == field,
                    iter(self.driver.find_elements(
                        By.CSS_SELECTOR,
                        'div[class*="oxd-grid-item oxd-grid-item--gutters"]'
                    ))
                ))[0]

                input = None
                if field == 'Employee Name':
                    input = tempElement.find_element(
                        By.CSS_SELECTOR,
                        'input[placeholder*="Type for hints..."]',
                    )
                else:
                    input = tempElement.find_element(
                        By.CSS_SELECTOR,
                        'input[class*="oxd-input oxd-input--active"]',
                    )
                input.click()
                input.send_keys(Keys.CONTROL + "a")
                input.send_keys(value)

            # Fill in dropdown_fields
            for field, value in dropdown_fields.items():
                dropdown = list(filter(lambda x: x.find_element(
                    By.CSS_SELECTOR,
                    'label[class="oxd-label"]'
                ).text == field,
                    iter(self.driver.find_elements(
                        By.CSS_SELECTOR,
                        'div[class="oxd-grid-item oxd-grid-item--gutters"]'
                    ))
                ))[0].find_element(
                    By.CSS_SELECTOR,
                    'div[class="oxd-select-text-input"]'
                )

                dropdown.click()

                item = list(filter(
                    lambda x: x.text == value if value != 'Select' else '-- Select --',
                    iter(self.driver.find_element(
                        By.CSS_SELECTOR,
                        'div[class^="oxd-select-dropdown"]'
                    ).find_elements(
                        By.CSS_SELECTOR,
                        "div"
                    ))
                ))[0]

                item.click()

            # Search for record
            search_button_element = self.driver.find_element(
                By.CSS_SELECTOR, 'button[class="oxd-button oxd-button--medium oxd-button--secondary orangehrm-left-space"]')

            search_button_element.click()

            result = int(result)
            if result != -1:
                num_res = len(self.driver.find_elements(
                    By.CSS_SELECTOR, 'div[class="oxd-table-card"]'))

                print("Expected value: {}".format(result))
                print("Received value: {}".format(num_res))
                assert num_res == result
            else:
                invalid_field_element = self.driver.find_element(
                    By.CSS_SELECTOR, 'span[class="oxd-text oxd-text--span oxd-input-field-error-message oxd-input-group__message"]')

                print("Expected value: 'Invalid'")
                print("Received value: '{}'".format(invalid_field_element.text))
                assert invalid_field_element.text == 'Invalid'

            print('TEST SUCCESS')
        except:
            print('TEST FAIL')
            self.driver.quit()
            raise



