import sys
import os

# Add the root directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import time
import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from pages.login_page import LoginPage
from pages.customised_page import CustomisedPage

class TestCustomised(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.get("https://www.demo.guru99.com/V4/")
        cls.driver.implicitly_wait(10)

        # Login before proceeding with tests
        login_page = LoginPage(cls.driver)
        login_page.enter_username("mngr599682")  # Update username
        login_page.enter_password("nyqEreh")     # Update password
        login_page.click_login()
        cls.driver.get("https://www.demo.guru99.com/V4/manager/CustomisedStatementInput.php")

    def load_page(self):
        """Loads the Customised Statement Input page."""
        self.driver.get("https://www.demo.guru99.com/V4/manager/CustomisedStatementInput.php")

    def setUp(self):
        """Runs before each test case."""
        self.load_page()
        self.customised_page = CustomisedPage(self.driver)

    def test_customised_empty(self):
        self.customised_page.enter_account_no("")  
        self.customised_page.enter_from_date("")  
        self.customised_page.enter_to_date("")  
        self.customised_page.enter_min_transaction_value("")  
        self.customised_page.enter_num_transaction("")  
        self.customised_page.click_submit()

        # Check for success alert
        try:
            WebDriverWait(self.driver, 10).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            self.assertEqual(alert.text, "Please fill all fields")
            alert.accept()
        except TimeoutException:
            print("No alert appeared.")

    def test_account_no_cannot_be_empty(self):
        self.customised_page.enter_account_no("")  # Empty account number
        self.customised_page.enter_from_date("01/10/2024")
        self.customised_page.enter_to_date("31/10/2024")
        self.customised_page.enter_min_transaction_value("500")
        self.customised_page.enter_num_transaction("5")
        
        error_message = self.driver.find_element(By.ID, "message2")  # ID theo thông báo lỗi thực tế
        self.assertTrue(error_message.is_displayed())
        self.assertEqual(error_message.text, "Account Number must not be blank")

    def test_account_no_characters_not_allowed(self):
        self.customised_page.enter_account_no("abc123") # Characters are not allowed
        self.customised_page.enter_from_date("01/10/2024")
        self.customised_page.enter_to_date("31/10/2024")
        self.customised_page.enter_min_transaction_value("500")
        self.customised_page.enter_num_transaction("5")
        
        error_message = self.driver.find_element(By.ID, "message2")  # ID theo thông báo lỗi thực tế
        self.assertTrue(error_message.is_displayed(), "Error message not displayed")
        self.assertEqual(error_message.text, "Characters are not allowed")

    def test_from_date_cannot_be_empty(self):
        self.customised_page.enter_account_no("139483")
        self.customised_page.enter_from_date("") # From Date Field must not be blank
        self.customised_page.enter_to_date("01/10/2024")
        self.customised_page.enter_min_transaction_value("500")
        self.customised_page.enter_num_transaction("5")
        
        error_message = self.driver.find_element(By.ID, "message26")  # ID theo thông báo lỗi thực tế
        self.assertTrue(error_message.is_displayed(), "Error message not displayed")
        self.assertEqual(error_message.text, "From Date Field must not be blank")

    def test_min_transaction_value_must_be_numeric(self):
        self.customised_page.enter_account_no("123456")
        self.customised_page.enter_from_date("01/10/2024")
        self.customised_page.enter_to_date("30/12/2024")
        self.customised_page.enter_min_transaction_value("five hundred") # Characters are not allowed
        self.customised_page.enter_num_transaction("5")
        
        error_message = self.driver.find_element(By.ID, "message12")  # ID theo thông báo lỗi thực tế
        self.assertTrue(error_message.is_displayed(), "Error message not displayed")
        self.assertEqual(error_message.text, "Characters are not allowed")

    def test_num_transaction_must_be_numeric(self):
        self.customised_page.enter_account_no("139483")
        self.customised_page.enter_from_date("01/10/2024")
        self.customised_page.enter_to_date("31/10/2024")
        self.customised_page.enter_min_transaction_value("500")
        self.customised_page.enter_num_transaction("five") # Characters are not allowed
        
        error_message = self.driver.find_element(By.ID, "message13")  # ID theo thông báo lỗi thực tế
        self.assertTrue(error_message.is_displayed(), "Error message not displayed")
        self.assertEqual(error_message.text, "Characters are not allowed")

    def test_reset_functionality(self):
        """Test the reset button functionality."""
        self.customised_page.enter_account_no("139483")
        self.customised_page.enter_from_date("01/10/2024")
        self.customised_page.enter_to_date("31/10/2024")
        self.customised_page.enter_min_transaction_value("500")
        self.customised_page.enter_num_transaction("5")
        self.customised_page.click_reset()

        # Assert fields are empty
        self.assertEqual(self.driver.find_element(*self.customised_page.account_no_input).get_attribute('value'), "")
        self.assertEqual(self.driver.find_element(*self.customised_page.from_date_input).get_attribute('value'), "")
        self.assertEqual(self.driver.find_element(*self.customised_page.to_date_input).get_attribute('value'), "")
        self.assertEqual(self.driver.find_element(*self.customised_page.min_transaction_value_input).get_attribute('value'), "")
        self.assertEqual(self.driver.find_element(*self.customised_page.num_transaction_input).get_attribute('value'), "")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()