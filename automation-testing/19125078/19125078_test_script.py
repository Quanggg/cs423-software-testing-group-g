import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import csv

class Login(unittest.TestCase):
    
    def setUp(self):
        if (browser == "1"):
            self.driver = webdriver.Edge()
        elif (browser == "2"):
            self.driver = webdriver.Firefox()
        else:
            self.driver = webdriver.Chrome()
        self.driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
        
    def test_correct_username_password(self):
        driver = self.driver
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        username = driver.find_element(By.NAME, "username")
        password = driver.find_element(By.NAME, "password")
        submit = driver.find_element(By.CLASS_NAME, "orangehrm-login-button")
        username.send_keys(loginDic["username"][1])
        password.send_keys(loginDic["password"][1])
        submit.click()
        self.assertNotIn("oxd-input-field-error-message", driver.page_source)
        self.assertNotIn("Invalid", driver.page_source)
        
    def test_empty_username_password(self):
        driver = self.driver
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        submit = driver.find_element(By.CLASS_NAME, "orangehrm-login-button")
        submit.click()
        self.assertIn("oxd-input-field-error-message", driver.page_source)
        
    def test_correct_username_wrong_password(self):
        driver = self.driver
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        username = driver.find_element(By.NAME, "username")
        password = driver.find_element(By.NAME, "password")
        submit = driver.find_element(By.CLASS_NAME, "orangehrm-login-button")
        username.send_keys(loginDic["username"][3])
        password.send_keys(loginDic["password"][3])
        submit.click()
        self.assertIn("Invalid", driver.page_source)
        
    def tearDown(self):
        self.driver.close()
        
class AddEmployee(unittest.TestCase):
    
    def setUp(self):
        if (browser == "1"):
            self.driver = webdriver.Edge()
        elif (browser == "2"):
            self.driver = webdriver.Firefox()
        else:
            self.driver = webdriver.Chrome()
        
        self.driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        username = self.driver.find_element(By.NAME, "username")
        password = self.driver.find_element(By.NAME, "password")
        submit = self.driver.find_element(By.CLASS_NAME, "orangehrm-login-button")
        username.send_keys(loginDic["username"][1])
        password.send_keys(loginDic["password"][1])
        submit.click()
        
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "oxd-main-menu-item-wrapper"))
        )
            
        pim_button = self.driver.find_elements(By.CLASS_NAME, "oxd-main-menu-item-wrapper")[1]

        pim_button.click()

        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "oxd-topbar-body-nav-tab-item"))
        )

        add_button = self.driver.find_elements(By.CLASS_NAME, "oxd-topbar-body-nav-tab-item")[2]

        add_button.click()
        
    def test_correct_data(self):
        driver = self.driver
        
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, "firstName"))
        )

        firstname = driver.find_element(By.NAME, "firstName")
        middlename = driver.find_element(By.NAME, "middleName")
        lastname = driver.find_element(By.NAME, "lastName")
        employeeid = driver.find_elements(By.CLASS_NAME, "oxd-input")[4]
        
        submit = driver.find_elements(By.CLASS_NAME, "oxd-button")[1]
        
        firstname.send_keys(addEmployeeDic["firstName"][1])
        middlename.send_keys(addEmployeeDic["middleName"][1])
        lastname.send_keys(addEmployeeDic["lastName"][1])
        employeeid.send_keys(addEmployeeDic["employeeId"][1])
        
        submit.click()
        
        WebDriverWait(driver, 10).until(
            EC.url_contains("viewPersonalDetails")
        )
        
    def test_empty_first_name(self):
        driver = self.driver
        
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, "firstName"))
        )

        firstname = driver.find_element(By.NAME, "firstName")
        middlename = driver.find_element(By.NAME, "middleName")
        lastname = driver.find_element(By.NAME, "lastName")
        employeeid = driver.find_elements(By.CLASS_NAME, "oxd-input")[4]
        
        submit = driver.find_elements(By.CLASS_NAME, "oxd-button")[1]
        
        firstname.send_keys(addEmployeeDic["firstName"][2])
        middlename.send_keys(addEmployeeDic["middleName"][2])
        lastname.send_keys(addEmployeeDic["lastName"][2])
        employeeid.send_keys(addEmployeeDic["employeeId"][2])
        
        submit.click()
        
        self.assertIn("Required", driver.page_source)
        
    def test_special_character_middle_name(self):
        driver = self.driver
        
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, "firstName"))
        )

        firstname = driver.find_element(By.NAME, "firstName")
        middlename = driver.find_element(By.NAME, "middleName")
        lastname = driver.find_element(By.NAME, "lastName")
        employeeid = driver.find_elements(By.CLASS_NAME, "oxd-input")[4]
        
        submit = driver.find_elements(By.CLASS_NAME, "oxd-button")[1]
        
        firstname.send_keys(addEmployeeDic["firstName"][3])
        middlename.send_keys(addEmployeeDic["middleName"][3])
        lastname.send_keys(addEmployeeDic["lastName"][3])
        employeeid.send_keys(addEmployeeDic["employeeId"][3])
        
        submit.click()
        
        self.assertIn("Invalid", driver.page_source)
        
    def test_number_last_name(self):
        driver = self.driver
        
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, "firstName"))
        )

        firstname = driver.find_element(By.NAME, "firstName")
        middlename = driver.find_element(By.NAME, "middleName")
        lastname = driver.find_element(By.NAME, "lastName")
        employeeid = driver.find_elements(By.CLASS_NAME, "oxd-input")[4]
        
        submit = driver.find_elements(By.CLASS_NAME, "oxd-button")[1]
        
        firstname.send_keys(addEmployeeDic["firstName"][4])
        middlename.send_keys(addEmployeeDic["middleName"][4])
        lastname.send_keys(addEmployeeDic["lastName"][4])
        employeeid.send_keys(addEmployeeDic["employeeId"][4])
        
        submit.click()
        
        self.assertIn("Invalid", driver.page_source)
        
    def test_11_characters_employee_id(self):
        driver = self.driver
        
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, "firstName"))
        )

        firstname = driver.find_element(By.NAME, "firstName")
        middlename = driver.find_element(By.NAME, "middleName")
        lastname = driver.find_element(By.NAME, "lastName")
        employeeid = driver.find_elements(By.CLASS_NAME, "oxd-input")[4]
        
        submit = driver.find_elements(By.CLASS_NAME, "oxd-button")[1]
        
        firstname.send_keys(addEmployeeDic["firstName"][5])
        middlename.send_keys(addEmployeeDic["middleName"][5])
        lastname.send_keys(addEmployeeDic["lastName"][5])
        employeeid.send_keys(addEmployeeDic["employeeId"][5])
        
        submit.click()
        
        self.assertNotIn("Should not exceed 10 characters", driver.page_source)
        
    def tearDown(self):
        self.driver.close()
        
if __name__ == "__main__":
    loginDic = dict()
    with open("login.csv",mode="r") as csv_file:
        csv_login = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_login:
            if line_count == 0:
                loginDic["username"] = [""]
                loginDic["password"] = [""]
                line_count += 1
            loginDic["username"].append(row["username"])
            loginDic["password"].append(row["password"])
            line_count += 1

    addEmployeeDic = dict()
    with open("add_employee.csv",mode="r") as csv_file:
        csv_addEmployee = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_addEmployee:
            if line_count == 0:
                addEmployeeDic["firstName"] = [""]
                addEmployeeDic["middleName"] = [""]
                addEmployeeDic["lastName"] = [""]
                addEmployeeDic["employeeId"] = [""]
                line_count += 1
            addEmployeeDic["firstName"].append(row["firstName"])
            addEmployeeDic["middleName"].append(row["middleName"])
            addEmployeeDic["lastName"].append(row["lastName"])
            addEmployeeDic["employeeId"].append(row["employeeId"])
            line_count += 1
    
    browser = input("Choose the browser you want to run tests (1: Edge, 2: Firefox, 3 and other: Chrome\n")
    unittest.main(verbosity=2, argv=["1"])