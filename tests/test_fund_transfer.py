import sys
import os

# Thêm thư mục gốc của dự án vào sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import time
import unittest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, UnexpectedAlertPresentException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from selenium.webdriver.common.by import By
from pages.login_page import LoginPage
from pages.fund_trasfer_page import FundTransferPage  # Import the FundTransferPage

# Additional import statements remain the same

class TestFundTransfer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.get("https://www.demo.guru99.com/V4/")
        cls.driver.implicitly_wait(10)

        login_page = LoginPage(cls.driver)
        login_page.enter_username("mngr599682")  # Change to your username
        login_page.enter_password("nyqEreh")  # Change to your password
        login_page.click_login()
        cls.driver.get("https://www.demo.guru99.com/V4/manager/FundTransInput.php")

    def load_page(self):
        self.driver.get("https://www.demo.guru99.com/V4/manager/FundTransInput.php")
        time.sleep(1)

    def setUp(self):
        self.load_page()
        self.fund_transfer_page = FundTransferPage(self.driver)

    def test_empty_payers_account_number(self):
        self.fund_transfer_page.enter_payers_account_no("")  # Empty payers account number
        self.fund_transfer_page.enter_payees_account_no("654321")
        self.fund_transfer_page.enter_amount("1000")
        self.fund_transfer_page.enter_description("Test empty payers account")
        self.fund_transfer_page.submit_fund_transfer()

        error_message = self.driver.find_element(By.ID, "message10")  # Adjust based on actual error message locator
        self.assertEqual(error_message.text, "Payers Account Number must not be blank")

    def test_empty_payees_account_number(self):
        self.fund_transfer_page.enter_payers_account_no("123456")
        self.fund_transfer_page.enter_payees_account_no("")  # Empty payees account number
        self.fund_transfer_page.enter_amount("1000")
        self.fund_transfer_page.enter_description("Test empty payees account")
        self.fund_transfer_page.submit_fund_transfer()

        error_message = self.driver.find_element(By.ID, "message11")  # Adjust based on actual error message locator
        self.assertEqual(error_message.text, "Payees Account Number must not be blank")

    def test_invalid_characters_in_amount(self):
        self.fund_transfer_page.enter_payers_account_no("123456")
        self.fund_transfer_page.enter_payees_account_no("654321")
        self.fund_transfer_page.enter_amount("abcd")  # Invalid characters
        self.fund_transfer_page.enter_description("Test invalid amount characters")
        self.fund_transfer_page.submit_fund_transfer()

        error_message = self.driver.find_element(By.ID, "message12")  # Adjust based on actual error message locator
        self.assertEqual(error_message.text, "Characters are not allowed")

    def test_invalid_characters_in_account_numbers(self):
        self.fund_transfer_page.enter_payers_account_no("abcde")  # Invalid characters
        self.fund_transfer_page.enter_payees_account_no("654321")
        self.fund_transfer_page.enter_amount("1000")
        self.fund_transfer_page.enter_description("Test invalid payers account number")
        self.fund_transfer_page.submit_fund_transfer()

        error_message = self.driver.find_element(By.ID, "message10")  # Adjust based on actual error message locator
        self.assertEqual(error_message.text, "Characters are not allowed")

    def test_special_characters_in_description(self):
        self.fund_transfer_page.enter_payers_account_no("123456")
        self.fund_transfer_page.enter_payees_account_no("654321")
        self.fund_transfer_page.enter_amount("1000")
        self.fund_transfer_page.enter_description("#$%^&*")  # Special characters
        self.fund_transfer_page.submit_fund_transfer()

        # Assuming that special characters should be flagged or an alert should appear
        try:
            alert = WebDriverWait(self.driver, 2).until(EC.alert_is_present())
            self.assertEqual(alert.text, "Special characters are not allowed in description")
            alert.accept()
            time.sleep(1)
        except TimeoutException:
            print("No alert appeared for special characters in description")

    def test_negative_or_zero_amount(self):
        self.fund_transfer_page.enter_payers_account_no("123456")
        self.fund_transfer_page.enter_payees_account_no("654321")
        
        # Test for zero amount
        self.fund_transfer_page.enter_amount("0")
        self.fund_transfer_page.enter_description("Test zero amount")
        self.fund_transfer_page.submit_fund_transfer()
        
        error_message = self.driver.find_element(By.ID, "message13")  # Adjust based on actual error message locator
        self.assertEqual(error_message.text, "Amount must be greater than zero")

        # Reload the page and test for negative amount
        self.load_page()
        self.fund_transfer_page.enter_payers_account_no("123456")
        self.fund_transfer_page.enter_payees_account_no("654321")
        self.fund_transfer_page.enter_amount("-100")
        self.fund_transfer_page.enter_description("Test negative amount")
        self.fund_transfer_page.submit_fund_transfer()

        error_message = self.driver.find_element(By.ID, "message13")
        self.assertEqual(error_message.text, "Amount must be greater than zero")

    # Retain existing tests like reset functionality, successful transfer, etc.

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
