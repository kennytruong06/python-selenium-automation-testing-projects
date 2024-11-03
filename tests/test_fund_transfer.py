import sys
import os

# Thêm thư mục gốc của dự án vào sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import time
import unittest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, UnexpectedAlertPresentException, NoAlertPresentException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By
from pages.login_page import LoginPage
from pages.fund_trasfer_page import FundTransferPage  # Import the FundTransferPage

# Additional import statements remain the same

class TestFundTransfer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(10)
        cls.driver.maximize_window()

    def load_page(self):
        self.driver.get("https://www.demo.guru99.com/V4/manager/FundTransInput.php")
        time.sleep(1)

    def setUp(self):
        self.load_page()
        self.fund_transfer_page = FundTransferPage(self.driver)

    def tearDown(self):
        try:
            alert = self.driver.switch_to.alert
            alert.accept()
        except NoAlertPresentException:
            pass

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
    
    def test_empty_all(self):
        self.fund_transfer_page.enter_payers_account_no("") 
        self.fund_transfer_page.enter_payees_account_no("")
        self.fund_transfer_page.enter_amount("")
        self.fund_transfer_page.enter_description("")
        self.fund_transfer_page.click_submit()

        try:
            WebDriverWait(self.driver, 10).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            self.assertEqual(alert.text, "Please fill all fields")
            alert.accept()
        except TimeoutException:
            print("No alert appeared.")
    
    def test_fill_all(self):
        self.fund_transfer_page.enter_payers_account_no("139483") 
        self.fund_transfer_page.enter_payees_account_no("139475")
        self.fund_transfer_page.enter_amount("100")
        self.fund_transfer_page.enter_description("hello")
        self.fund_transfer_page.click_submit()

        try:
            WebDriverWait(self.driver, 10).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            self.assertEqual(alert.text, "You are not authorize to do fund transfer!!")
            alert.accept()
        except TimeoutException:
            print("No alert appeared.")

    def test_empty_payers_account_number(self):
        self.fund_transfer_page.enter_payers_account_no("")  # Empty payers account number
        self.fund_transfer_page.enter_payees_account_no("654321")
        self.fund_transfer_page.enter_amount("1000")
        self.fund_transfer_page.enter_description("Test empty payers account")
        

        error_message = self.driver.find_element(By.ID, "message10")  # ID theo thông báo lỗi thực tế
        self.assertTrue(error_message.is_displayed(), "Error message not displayed")
        self.assertEqual(error_message.text, "Payers Account Number must not be blank")

    def test_empty_payees_account_number(self):
        self.fund_transfer_page.enter_payers_account_no("123456")
        self.fund_transfer_page.enter_payees_account_no("")  # Empty payees account number
        self.fund_transfer_page.enter_amount("1000")
        self.fund_transfer_page.enter_description("Test empty payees account")
        

        error_message = self.driver.find_element(By.ID, "message11")  # ID theo thông báo lỗi thực tế
        self.assertTrue(error_message.is_displayed(), "Error message not displayed")
        self.assertEqual(error_message.text, "Payees Account Number must not be blank")

    def test_invalid_characters_in_amount(self):
        self.fund_transfer_page.enter_payers_account_no("123456")
        self.fund_transfer_page.enter_payees_account_no("654321")
        self.fund_transfer_page.enter_amount("abcd")  # Invalid characters
        self.fund_transfer_page.enter_description("Test invalid amount characters")
        

        error_message = self.driver.find_element(By.ID, "message1")  # ID theo thông báo lỗi thực tế
        self.assertTrue(error_message.is_displayed(), "Error message not displayed")
        self.assertEqual(error_message.text, "Characters are not allowed")

    def test_invalid_characters_in_account_numbers(self):
        self.fund_transfer_page.enter_payers_account_no("abcde")  # Invalid characters
        self.fund_transfer_page.enter_payees_account_no("654321")
        self.fund_transfer_page.enter_amount("1000")
        self.fund_transfer_page.enter_description("Test invalid payers account number")
        

        error_message = self.driver.find_element(By.ID, "message10")  # ID theo thông báo lỗi thực tế
        self.assertTrue(error_message.is_displayed(), "Error message not displayed")
        self.assertEqual(error_message.text, "Characters are not allowed")
                

    def test_negative_or_zero_amount(self):
        self.fund_transfer_page.enter_payers_account_no("123456")
        self.fund_transfer_page.enter_payees_account_no("654321")
        
        # Test for zero amount
        self.fund_transfer_page.enter_amount("0")
        self.fund_transfer_page.enter_description("Test zero amount")
        self.fund_transfer_page.click_submit()
        
        try:
            WebDriverWait(self.driver, 10).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            self.assertEqual(alert.text, "You are not authorize to do fund transfer!!")
            alert.accept()
        except TimeoutException:
            print("No alert appeared.")

        # Reload the page and test for negative amount
        self.load_page()
        self.fund_transfer_page.enter_payers_account_no("123456")
        self.fund_transfer_page.enter_payees_account_no("654321")
        self.fund_transfer_page.enter_amount("-1000")
        self.fund_transfer_page.enter_description("Test negative amount")
        self.fund_transfer_page.click_submit()

        try:
            WebDriverWait(self.driver, 10).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            self.assertEqual(alert.text, "You are not authorize to do fund transfer!!")
            alert.accept()
        except TimeoutException:
            print("No alert appeared.")

if __name__ == "__main__":
    unittest.main()