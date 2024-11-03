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
from pages.withdrawal_page import WithdrawalPage

class TestWithdrawal(unittest.TestCase):
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
        cls.driver.get("https://www.demo.guru99.com/V4/manager/WithdrawalInput.php")

    def load_page(self):
        """Loads the Withdrawal page."""
        self.driver.get("https://www.demo.guru99.com/V4/manager/WithdrawalInput.php")

    def setUp(self):
        """Runs before each test case."""
        self.load_page()
        self.withdrawal_page = WithdrawalPage(self.driver)

    # Test cases
    def test_submit_empty_fields(self):
        """Test alert for all fields left empty"""
        self.withdrawal_page.click_submit()
        try:
            WebDriverWait(self.driver, 10).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            self.assertEqual(alert.text, "Please fill all fields")
            alert.accept()
        except TimeoutException:
            print("No alert appeared.")

    def test_empty_account_no(self):
        """Test error when Account No is left empty"""
        self.withdrawal_page.enter_account_no("")
        self.withdrawal_page.enter_amount("1000")
        self.withdrawal_page.enter_description("Test Withdrawal")
        
        error_message = self.driver.find_element(By.ID, "message2")
        self.assertTrue(error_message.is_displayed())
        self.assertEqual(error_message.text, "Account Number must not be blank")

    def test_account_no_characters_not_allowed(self):
        """Test error for non-numeric Account No"""
        self.withdrawal_page.enter_account_no("abc123")
        self.withdrawal_page.enter_amount("1000")
        self.withdrawal_page.enter_description("Test Withdrawal")
        
        error_message = self.driver.find_element(By.ID, "message2")
        self.assertTrue(error_message.is_displayed())
        self.assertEqual(error_message.text, "Characters are not allowed")

    def test_empty_amount(self):
        """Test error when Amount is left empty"""
        self.withdrawal_page.enter_account_no("123456")
        self.withdrawal_page.enter_amount("")
        self.withdrawal_page.enter_description("Test Withdrawal")
        
        error_message = self.driver.find_element(By.ID, "message1")
        self.assertTrue(error_message.is_displayed())
        self.assertEqual(error_message.text, "Amount field must not be blank")

    def test_amount_characters_not_allowed(self):
        """Test error for non-numeric Amount"""
        self.withdrawal_page.enter_account_no("123456")
        self.withdrawal_page.enter_amount("one thousand")
        self.withdrawal_page.enter_description("Test Withdrawal")
        
        error_message = self.driver.find_element(By.ID, "message1")
        self.assertTrue(error_message.is_displayed())
        self.assertEqual(error_message.text, "Characters are not allowed")

    def test_valid_withdrawal_submission(self):
        """Test successful submission with valid data"""
        self.withdrawal_page.enter_account_no("123456")
        self.withdrawal_page.enter_amount("1000")
        self.withdrawal_page.enter_description("Test Withdrawal")
        self.withdrawal_page.click_submit()

        try:
            alert = WebDriverWait(self.driver, 2).until(EC.alert_is_present())
            self.assertEqual(alert.text, "Account does not exist")
            alert.accept()
            time.sleep(1)
        except TimeoutException:
            print("No alert appeared.")

    def test_reset_functionality(self):
        """Test the reset button functionality"""
        self.withdrawal_page.enter_account_no("123456")
        self.withdrawal_page.enter_amount("1000")
        self.withdrawal_page.enter_description("Test Withdrawal")
        self.withdrawal_page.click_reset()

        # Assert fields are empty
        self.assertEqual(self.driver.find_element(*self.withdrawal_page.account_no_input).get_attribute('value'), "")
        self.assertEqual(self.driver.find_element(*self.withdrawal_page.amount_input).get_attribute('value'), "")
        self.assertEqual(self.driver.find_element(*self.withdrawal_page.description_input).get_attribute('value'), "")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
