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
from pages.deposit_page import DepositPage  # Đổi tên import thành DepositPage

class TestDeposit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.get("https://www.demo.guru99.com/V4/")
        cls.driver.implicitly_wait(10)

        # Đăng nhập trước khi kiểm tra
        login_page = LoginPage(cls.driver)
        login_page.enter_username("mngr599682")  # Thay đổi theo tên người dùng của bạn
        login_page.enter_password("nyqEreh")  # Thay đổi theo mật khẩu của bạn
        login_page.click_login()
        cls.driver.get("https://www.demo.guru99.com/V4/manager/DepositInput.php")

    def load_page(self):
        """Hàm này sẽ tải lại trang DepositInput."""
        self.driver.get("https://www.demo.guru99.com/V4/manager/DepositInput.php")
        time.sleep(1)

    def setUp(self):
        """Hàm này sẽ chạy trước mỗi test case."""
        self.load_page()
        self.deposit_page = DepositPage(self.driver)

    def test_deposit_successful(self):
        self.deposit_page.enter_account_number("123456")  # Số tài khoản hợp lệ
        self.deposit_page.enter_amount("1000")  # Số tiền hợp lệ
        self.deposit_page.enter_description("Test Deposit")  # Mô tả giao dịch
        self.deposit_page.click_submit()

        try:
            alert = WebDriverWait(self.driver, 2).until(EC.alert_is_present())
            self.assertEqual(alert.text, "Account does not exist")
            alert.accept()
            time.sleep(1)
        except TimeoutException:
            print("No alert appeared.")

    def test_deposit_with_empty_fields(self):
        self.deposit_page.enter_account_number("")  # Để trống số tài khoản
        self.deposit_page.enter_amount("")  # Để trống số tiền
        self.deposit_page.enter_description("")  # Để trống mô tả
        self.deposit_page.click_submit()

        try:
            alert = WebDriverWait(self.driver, 2).until(EC.alert_is_present())
            self.assertEqual(alert.text, "Please fill all fields")
            alert.accept()
            time.sleep(1)
        except TimeoutException:
            print("No alert appeared.")

    ## Account No
    def test_deposit_account_no_should_be_validate_empty(self):
        self.deposit_page.enter_account_number("")
        self.deposit_page.enter_amount("1000")  # Loại tài khoản hợp lệ
        self.deposit_page.enter_description("tesst")  # Số tiền gửi hợp lệ

        error_message = self.driver.find_element(By.ID, "message2")
        self.assertEqual(error_message.text, "Account Number must not be blank")

    def test_deposit_account_no_should_be_validate_characters_not_allowed(self):
        self.deposit_page.enter_account_number("asdfasd")
        self.deposit_page.enter_amount("1000")  # Loại tài khoản hợp lệ
        self.deposit_page.enter_description("tesst")  # Số tiền gửi hợp lệ

        error_message = self.driver.find_element(By.ID, "message2")
        self.assertEqual(error_message.text, "Characters are not allowed")

    def test_deposit_account_no_should_be_validate_special_characters_not_allowed(self):
        self.deposit_page.enter_account_number("#%$^%$%")
        self.deposit_page.enter_amount("1000")  # Loại tài khoản hợp lệ
        self.deposit_page.enter_description("tesst")  # Số tiền gửi hợp lệ

        error_message = self.driver.find_element(By.ID, "message2")
        self.assertEqual(error_message.text, "Special characters are not allowed")

    ## Amount
    def test_deposit_amount_should_be_validate_empty(self):
        self.deposit_page.enter_account_number("12345")
        self.deposit_page.enter_amount("")  # Loại tài khoản hợp lệ
        self.deposit_page.enter_description("tesst")  # Số tiền gửi hợp lệ

        error_message = self.driver.find_element(By.ID, "message1")
        self.assertEqual(error_message.text, "Amount field must not be blank")

    def test_deposit_amount_should_be_validate_characters_not_allowed(self):
        self.deposit_page.enter_account_number("1234")
        self.deposit_page.enter_amount("dfgsdfgsdfg")  # Loại tài khoản hợp lệ
        self.deposit_page.enter_description("tesst")  # Số tiền gửi hợp lệ

        error_message = self.driver.find_element(By.ID, "message1")
        self.assertEqual(error_message.text, "Characters are not allowed")

    def test_deposit_amount_should_be_validate_special_characters_not_allowed(self):
        self.deposit_page.enter_account_number("123")
        self.deposit_page.enter_amount("#@#@$")  # Loại tài khoản hợp lệ
        self.deposit_page.enter_description("tesst")  # Số tiền gửi hợp lệ

        error_message = self.driver.find_element(By.ID, "message1")
        self.assertEqual(error_message.text, "Special characters are not allowed")


    ## Description
    def test_description_should_be_validate_empty(self):
        self.deposit_page.enter_description("")
        self.deposit_page.enter_account_number("12345")
        self.deposit_page.enter_amount("1000")

        error_message = self.driver.find_element(By.ID, "message17")
        self.assertEqual(error_message.text, "Description can not be blank")












    def test_reset_functionality(self):
        """Kiểm tra chức năng nút Reset."""
        # Nhập thông tin vào các trường
        self.deposit_page.enter_account_number("12345678")
        self.deposit_page.enter_amount("1000")
        self.deposit_page.enter_description("Deposit for savings")

        # Nhấn nút Reset
        self.deposit_page.click_reset()

        # Kiểm tra các trường đã trở về trạng thái ban đầu
        account_number_value = self.driver.find_element(*self.deposit_page.account_number_field).get_attribute('value')
        amount_value = self.driver.find_element(*self.deposit_page.amount_field).get_attribute('value')
        description_value = self.driver.find_element(*self.deposit_page.description_field).get_attribute('value')

        self.assertEqual(account_number_value, "", "Account Number field should be empty after reset")
        self.assertEqual(amount_value, "", "Amount field should be empty after reset")
        self.assertEqual(description_value, "", "Description field should be empty after reset")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
