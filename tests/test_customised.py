# tests/test_customised.py
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
        login_page.enter_username("mngr599682")  # Change this to your username
        login_page.enter_password("nyqEreh")  # Change this to your password
        login_page.click_login()
        cls.driver.get("https://www.demo.guru99.com/V4/manager/CustomisedStatementInput.php")

    def load_page(self):
        """Loads the Customised Statement Input page."""
        self.driver.get("https://www.demo.guru99.com/V4/manager/CustomisedStatementInput.php")
        time.sleep(1)

    def setUp(self):
        """Runs before each test case."""
        self.load_page()
        self.customised_page = CustomisedPage(self.driver)

    def test_customised_successful(self):
        self.customised_page.enter_account_no("123456")  # Valid account number
        self.customised_page.enter_from_date("01/01/2024")  # Valid From Date
        self.customised_page.enter_to_date("12/12/2024")  # Valid To Date
        self.customised_page.enter_min_transaction_value("500")  # Valid Minimum Transaction Value
        self.customised_page.enter_num_transaction("5")  # Valid Number of Transactions
        self.customised_page.click_submit()

        # Check for success alert
        try:
            alert = WebDriverWait(self.driver, 2).until(EC.alert_is_present())
            self.assertEqual(alert.text, "Statement generated successfully")
            alert.accept()
            time.sleep(1)
        except TimeoutException:
            print("No alert appeared.")

    # New Test Cases Below
    def test_account_no_cannot_be_empty(self):
        self.customised_page.enter_account_no("")  # Empty account number
        self.customised_page.enter_from_date("01/01/2024")
        self.customised_page.enter_to_date("12/12/2024")
        self.customised_page.enter_min_transaction_value("500")
        self.customised_page.enter_num_transaction("5")
        self.customised_page.click_submit()

        error_message = self.driver.find_element(By.ID, "message2").text
        self.assertEqual(error_message, "Account Number must not be blank")

    def test_account_no_characters_not_allowed(self):
        self.customised_page.enter_account_no("abc123")
        self.customised_page.enter_from_date("01/01/2024")
        self.customised_page.enter_to_date("12/12/2024")
        self.customised_page.enter_min_transaction_value("500")
        self.customised_page.enter_num_transaction("5")
        self.customised_page.click_submit()

        error_message = self.driver.find_element(By.ID, "message2").text
        self.assertEqual(error_message, "Characters are not allowed")

    def test_from_date_cannot_be_empty(self):
        self.customised_page.enter_account_no("123456")
        self.customised_page.enter_from_date("")
        self.customised_page.enter_to_date("12/12/2024")
        self.customised_page.enter_min_transaction_value("500")
        self.customised_page.enter_num_transaction("5")
        self.customised_page.click_submit()

        error_message = self.driver.find_element(By.ID, "message3").text
        self.assertEqual(error_message, "From Date field must not be blank")

    def test_invalid_from_date_format(self):
        self.customised_page.enter_account_no("123456")
        self.customised_page.enter_from_date("2024/01/01")  # Invalid format
        self.customised_page.enter_to_date("12/12/2024")
        self.customised_page.enter_min_transaction_value("500")
        self.customised_page.enter_num_transaction("5")
        self.customised_page.click_submit()

        error_message = self.driver.find_element(By.ID, "message3").text
        self.assertEqual(error_message, "Date format should be MM/DD/YYYY")

    def test_min_transaction_value_must_be_numeric(self):
        self.customised_page.enter_account_no("123456")
        self.customised_page.enter_from_date("01/01/2024")
        self.customised_page.enter_to_date("12/12/2024")
        self.customised_page.enter_min_transaction_value("five hundred")  # Invalid non-numeric value
        self.customised_page.enter_num_transaction("5")
        self.customised_page.click_submit()

        error_message = self.driver.find_element(By.ID, "message4").text
        self.assertEqual(error_message, "Minimum Transaction Value must be numeric")

    def test_num_transaction_must_be_numeric(self):
        self.customised_page.enter_account_no("123456")
        self.customised_page.enter_from_date("01/01/2024")
        self.customised_page.enter_to_date("12/12/2024")
        self.customised_page.enter_min_transaction_value("500")
        self.customised_page.enter_num_transaction("five")  # Invalid non-numeric value
        self.customised_page.click_submit()

        error_message = self.driver.find_element(By.ID, "message5").text
        self.assertEqual(error_message, "Number of Transaction must be numeric")

    def test_reset_functionality(self):
        """Test the reset button functionality."""
        self.customised_page.enter_account_no("123456")
        self.customised_page.enter_from_date("01/01/2024")
        self.customised_page.enter_to_date("12/12/2024")
        self.customised_page.enter_min_transaction_value("500")
        self.customised_page.enter_num_transaction("5")

        # Click the reset button
        self.customised_page.click_reset()

        # Check if fields are empty
        account_no_value = self.driver.find_element(*self.customised_page.account_no_input).get_attribute('value')
        from_date_value = self.driver.find_element(*self.customised_page.from_date_input).get_attribute('value')
        to_date_value = self.driver.find_element(*self.customised_page.to_date_input).get_attribute('value')
        min_transaction_value = self.driver.find_element(*self.customised_page.min_transaction_value_input).get_attribute('value')
        num_transaction_value = self.driver.find_element(*self.customised_page.num_transaction_input).get_attribute('value')

        self.assertEqual(account_no_value, "", "Account Number field should be empty after reset")
        self.assertEqual(from_date_value, "", "From Date field should be empty after reset")
        self.assertEqual(to_date_value, "", "To Date field should be empty after reset")
        self.assertEqual(min_transaction_value, "", "Minimum Transaction Value field should be empty after reset")
        self.assertEqual(num_transaction_value, "", "Number of Transactions field should be empty after reset")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
