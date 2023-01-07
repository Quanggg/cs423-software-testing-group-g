import unittest
from constant import ORANGEHRM_URL, USERNAME, PASSWORD, CHROME_WEBDRIVER_PATH, EDGE_WEBDRIVER_PATH, FIREFOX_WEBDRIVER_PATH
from ddt import ddt, data, unpack
from selenium import webdriver
from selenium.webdriver.common.by import By
from utils import get_csv_data


@ddt
class CandidateRecruitmentTest(unittest.TestCase):
    def setUp(self) -> None:
        self.driver = webdriver.Chrome(CHROME_WEBDRIVER_PATH)
        # self.driver = webdriver.Edge(EDGE_WEBDRIVER_PATH)
        # self.driver = webdriver.Firefox(FIREFOX_WEBDRIVER_PATH)
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

    def addNewCandidate(self) -> None:
        recruitmentTabEl = self.driver.find_element(
            By.CSS_SELECTOR, "a[href='/web/index.php/recruitment/viewRecruitmentModule']")
        recruitmentTabEl.click()

        addBtn = self.driver.find_element(
            By.XPATH, "//button[@class='oxd-button oxd-button--medium oxd-button--secondary']")
        addBtn.click()

        return

    @data(*get_csv_data("candidate_data.csv"))
    @unpack
    def test_recruit_candidate(self, fname='', mname='', lname='', vacancy='', email='', contact='', note='') -> None:
        try:
            self.addNewCandidate()

            # find elements
            fnameEl = self.driver.find_element(By.NAME, "firstName")
            mnameEl = self.driver.find_element(By.NAME, "middleName")
            lnameEl = self.driver.find_element(By.NAME, "lastName")
            vacancyEl = self.driver.find_element(
                By.XPATH, "//div[@class='oxd-select-text-input']")
            inputEls = self.driver.find_elements(
                By.XPATH, "//input[@placeholder='Type here']")
            emailEl = inputEls[0]
            contactEl = inputEls[1]
            noteEl = self.driver.find_element(
                By.XPATH, "//textarea[@placeholder='Type here']")
            consentEl = self.driver.find_element(
                By.XPATH, "//span[@class='oxd-checkbox-input oxd-checkbox-input--active --label-right oxd-checkbox-input']")
            saveBtn = self.driver.find_element(
                By.XPATH, "//button[@type='submit']")

            # set value for input
            fnameEl.send_keys(fname)
            mnameEl.send_keys(mname)
            lnameEl.send_keys(lname)
            emailEl.send_keys(email)
            contactEl.send_keys(contact)
            noteEl.send_keys(note)

            saveBtn.click()

            errorEls = self.driver.find_elements(
                By.XPATH, "//span[@class='oxd-text oxd-text--span oxd-input-field-error-message oxd-input-group__message']")
            assert errorEls.__len__() == 0

        except:
            self.tearDown()
            raise

        return
