import sys
import os

# Thêm thư mục gốc của dự án vào sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from selenium import webdriver
from pages.login_page import LoginPage
from pages.withdraw_pages import WithdrawPage


class TestWithdraw(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://www.demo.guru99.com/V4/")
        login_page = LoginPage(self.driver)
        login_page.enter_username("mngr599682")
        login_page.enter_password("nyqEreh")
        login_page.click_login()
        self.driver.get("https://www.demo.guru99.com/V4/manager/WithdrawalInput.php")
        self.withdraw_page = WithdrawPage(self.driver)

    def test_withdraw_successful(self):
        self.withdraw_page.enter_account_number("123456")
        self.withdraw_page.enter_amount("500")
        self.withdraw_page.enter_description("Test withdrawal")
        self.withdraw_page.click_submit()
        self.assertIn("Transaction details of Withdrawal for Account", self.driver.page_source)

    def test_withdraw_invalid_account_number(self):
        self.withdraw_page.enter_account_number("invalid")
        self.withdraw_page.enter_amount("500")
        self.withdraw_page.enter_description("Test withdrawal")
        self.withdraw_page.click_submit()
        self.assertIn("Account does not exist", self.driver.page_source)

    def test_withdraw_insufficient_funds(self):
        self.withdraw_page.enter_account_number("123456")
        self.withdraw_page.enter_amount("1000000")
        self.withdraw_page.enter_description("Test withdrawal")
        self.withdraw_page.click_submit()
        self.assertIn("Insufficient funds", self.driver.page_source)

    def test_withdraw_empty_fields(self):
        self.withdraw_page.click_submit()
        self.assertIn("Please fill all fields", self.driver.page_source)

    def test_withdraw_special_characters(self):
        self.withdraw_page.enter_account_number("123456")
        self.withdraw_page.enter_amount("500$")
        self.withdraw_page.enter_description("Test withdrawal")
        self.withdraw_page.click_submit()
        self.assertIn("Special characters are not allowed", self.driver.page_source)

    def test_withdraw_characters_not_allowed(self):
        self.withdraw_page.enter_account_number("123456")
        self.withdraw_page.enter_amount("five hundred")
        self.withdraw_page.enter_description("Test withdrawal")
        self.withdraw_page.click_submit()
        self.assertIn("Characters are not allowed", self.driver.page_source)

    def test_withdraw_reset(self):
        self.withdraw_page.enter_account_number("123456")
        self.withdraw_page.enter_amount("500")
        self.withdraw_page.enter_description("Test withdrawal")
        self.withdraw_page.click_reset()
        self.assertEqual(self.withdraw_page.driver.find_element(*self.withdraw_page.account_number_field).get_attribute('value'), '')
        self.assertEqual(self.withdraw_page.driver.find_element(*self.withdraw_page.amount_field).get_attribute('value'), '')
        self.assertEqual(self.withdraw_page.driver.find_element(*self.withdraw_page.description_field).get_attribute('value'), '')


    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()