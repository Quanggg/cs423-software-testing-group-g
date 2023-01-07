import time
import unittest
from constant import ORANGEHRM_URL, USERNAME, PASSWORD, CHROME_WEBDRIVER_PATH, EDGE_WEBDRIVER_PATH, FIREFOX_WEBDRIVER_PATH
from ddt import ddt, data, unpack
from selenium import webdriver
from selenium.webdriver.common.by import By
from utils import get_csv_data

import random


@ddt
class VacancyAddTest(unittest.TestCase):
    def setUp(self) -> None:
        self.driver = webdriver.Chrome(CHROME_WEBDRIVER_PATH)
        # self.driver = webdriver.Edge(EDGE_WEBDRIVER_PATH)
        # self.driver = webdriver.Firefox(FIREFOX_WEBDRIVER_PATH
        self.driver.implicitly_wait(5)
        self.driver.get(ORANGEHRM_URL)
        self.login()

        return

    def tearDown(self) -> None:
        self.driver.quit()

        return

    def login(self) -> None:
        usernameEl = self.driver.find_element(By.NAME, 'username')
        pwdEl = self.driver.find_element(By.NAME, 'password')
        usernameEl.send_keys(USERNAME)
        pwdEl.send_keys(PASSWORD)
        pwdEl.submit()

        return

    def addNewVacancy(self) -> None:
        recruitmentTabEl = self.driver.find_element(
            By.CSS_SELECTOR, "a[href='/web/index.php/recruitment/viewRecruitmentModule']")
        recruitmentTabEl.click()
        vacancyTabEl = self.driver.find_element(
            By.XPATH, "//li[@class='oxd-topbar-body-nav-tab']")
        vacancyTabEl.click()
        addBtn = self.driver.find_element(
            By.XPATH, "//button[@class='oxd-button oxd-button--medium oxd-button--secondary']")
        addBtn.click()

        return

    @data(*get_csv_data("vacancy_data.csv"))
    @unpack
    def test_add_vacancy(self, vacancy='', jobIdx=0, description='', hiringManager='A', numOfPosition=0, active=1, publish=1) -> None:
        try:
            jobIdx = int(jobIdx)
            active = int(active)
            publish = int(publish)

            self.addNewVacancy()

            # find elements
            vacancyEl = self.driver.find_elements(
                By.XPATH, "//input[@class='oxd-input oxd-input--active']")[-2]
            descriptionEl = self.driver.find_element(By.TAG_NAME, "textarea")
            jobTitleEl = self.driver.find_element(
                By.XPATH, "//div[@class='oxd-select-text-input']")
            numOfPosEl = self.driver.find_elements(
                By.XPATH, "//input[@class='oxd-input oxd-input--active']")[-1]
            hiringManagerEl = self.driver.find_element(
                By.XPATH, "//input[@placeholder='Type for hints...']")
            checkBoxEl = self.driver.find_elements(
                By.XPATH, "//span[@class='oxd-switch-input oxd-switch-input--active --label-right']")
            saveBtn = self.driver.find_element(
                By.XPATH, "//button[@type='submit']")

            # set value
            num = random.randint(0, 1000)
            if (vacancy.__len__() > 0):
                vacancyEl.send_keys(vacancy+num.__str__())
            jobTitleEl.click()
            time.sleep(0.5)
            jobTitleOptions = self.driver.find_elements(
                By.XPATH, "//div[@role='option']")
            assert jobIdx >= 0
            if (jobIdx >= jobTitleOptions.__len__()):
                jobIdx = -1
            jobTitleOptions[jobIdx].click()
            descriptionEl.send_keys(description)
            numOfPosEl.send_keys(numOfPosition)
            hiringManagerEl.send_keys(hiringManager)
            time.sleep(3)  # sleep for searching
            hiringManagerOptions = self.driver.find_elements(
                By.XPATH, "//div[@role='option']")
            try:
                hiringManagerOptions[0].click()
            except:
                None
            if (active == False):
                checkBoxEl[0].click()
            if (publish == False):
                checkBoxEl[1].click()
            saveBtn.click()

            errorEls = self.driver.find_elements(
                By.XPATH, "//span[@class='oxd-text oxd-text--span oxd-input-field-error-message oxd-input-group__message']")
            assert errorEls.__len__() == 0
        except:
            self.tearDown()
            raise

        return
