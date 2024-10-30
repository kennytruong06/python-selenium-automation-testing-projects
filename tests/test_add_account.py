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
from pages.add_account_page import AddAccountPage

class TestAddAccount(unittest.TestCase):
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
        cls.driver.get("https://www.demo.guru99.com/V4/manager/addAccount.php")

    def load_page(self):
        """Hàm này sẽ tải lại trang add account."""
        self.driver.get("https://www.demo.guru99.com/V4/manager/addAccount.php")
        time.sleep(1)

    def setUp(self):
        """Hàm này sẽ chạy trước mỗi test case."""
        self.load_page()
        self.add_account_page = AddAccountPage(self.driver)

    def test_add_account_successful(self):
        self.add_account_page.enter_customer_id(12345)  # ID khách hàng hợp lệ
        self.add_account_page.select_account_type("Savings")  # Loại tài khoản hợp lệ
        self.add_account_page.enter_initial_deposit("1000")  # Số tiền gửi hợp lệ
        self.add_account_page.click_submit()

        try:
            alert = WebDriverWait(self.driver, 2).until(EC.alert_is_present())
            self.assertEqual(alert.text, "Customer does not exist!!")
            alert.accept()
            time.sleep(1)
        except TimeoutException:
            print("No alert appeared.")

    def test_add_account_with_empty_fields(self):
        self.add_account_page.enter_customer_id("")  # Để trống ID khách hàng
        self.add_account_page.select_account_type("Savings")  # Loại tài khoản hợp lệ
        self.add_account_page.enter_initial_deposit("")  # Để trống số tiền gửi
        self.add_account_page.click_submit()

        try:
            alert = WebDriverWait(self.driver, 2).until(EC.alert_is_present())
            self.assertEqual(alert.text, "Please fill all fields")
            alert.accept()
            time.sleep(1)
        except TimeoutException:
            print("No alert appeared.")

    def test_add_account_customer_id_should_be_validate_empty(self):
        self.add_account_page.enter_customer_id("")
        self.add_account_page.select_account_type("Savings")  # Loại tài khoản hợp lệ
        self.add_account_page.enter_initial_deposit("1000")  # Số tiền gửi hợp lệ

        error_message = self.driver.find_element(By.ID, "message14")  # ID theo thông báo lỗi thực tế
        self.assertTrue(error_message.is_displayed(), "Error message not displayed")
        self.assertEqual(error_message.text, "Customer ID is required")

    def test_add_account_customer_id_should_be_validate_characters_not_allowed(self):
        self.add_account_page.enter_customer_id("dsfsd")
        self.add_account_page.select_account_type("Savings")  # Loại tài khoản hợp lệ
        self.add_account_page.enter_initial_deposit("1000")  # Số tiền gửi hợp lệ

        error_message = self.driver.find_element(By.ID, "message14")  # ID theo thông báo lỗi thực tế
        self.assertTrue(error_message.is_displayed(), "Error message not displayed")
        self.assertEqual(error_message.text, "Characters are not allowed")

    def test_add_account_customer_id_should_be_validate_special_characters_not_allowed(self):
        self.add_account_page.enter_customer_id("&$@%^")
        self.add_account_page.select_account_type("Savings")  # Loại tài khoản hợp lệ
        self.add_account_page.enter_initial_deposit("1000")  # Số tiền gửi hợp lệ

        error_message = self.driver.find_element(By.ID, "message14")  # ID theo thông báo lỗi thực tế
        self.assertTrue(error_message.is_displayed(), "Error message not displayed")
        self.assertEqual(error_message.text, "Special characters are not allowed")


    def test_add_account_initial_deposit_should_be_validate_empty(self):
        self.add_account_page.enter_initial_deposit("")  # Số tiền gửi hợp lệ
        self.add_account_page.enter_customer_id("12345")
        self.add_account_page.select_account_type("Savings")  # Loại tài khoản hợp lệ

        error_message = self.driver.find_element(By.ID, "message19")  # ID theo thông báo lỗi thực tế
        self.assertEqual(error_message.text, "Initial Deposit must not be blank")

    def test_add_account_initial_deposit_should_be_validate_characters_not_allowed(self):
        self.add_account_page.enter_initial_deposit("dsfsd")  # Số tiền gửi hợp lệ
        self.add_account_page.enter_customer_id("1234")
        self.add_account_page.select_account_type("Savings")  # Loại tài khoản hợp lệ

        error_message = self.driver.find_element(By.ID, "message19")
        self.assertEqual(error_message.text, "Characters are not allowed")

    def test_add_account_initial_deposit_should_be_validate_special_characters_not_allowed(self):
        self.add_account_page.enter_initial_deposit("&$@%^")
        self.add_account_page.enter_customer_id("12345")
        self.add_account_page.select_account_type("Savings")

        error_message = self.driver.find_element(By.ID, "message19")
        self.assertEqual(error_message.text, "Special characters are not allowed")



    def test_reset_functionality(self):
        """Kiểm tra chức năng nút Reset."""
        # Nhập thông tin vào các trường
        self.add_account_page.enter_customer_id("12345")
        self.add_account_page.select_account_type("Current")
        self.add_account_page.enter_initial_deposit("1000")

        # Nhấn nút Reset
        self.add_account_page.click_reset()

        # Kiểm tra các trường đã trở về trạng thái ban đầu
        customer_id_value = self.driver.find_element(*self.add_account_page.customer_id_field).get_attribute('value')
        initial_deposit_value = self.driver.find_element(*self.add_account_page.initial_deposit_field).get_attribute(
            'value')

        self.assertEqual(customer_id_value, "", "Customer ID field should be empty after reset")
        self.assertEqual(initial_deposit_value, "", "Initial Deposit field should be empty after reset")

        # Kiểm tra xem loại tài khoản có trở về giá trị mặc định không
        account_type_dropdown = self.driver.find_element(*self.add_account_page.account_type_dropdown)
        default_selected_option = account_type_dropdown.find_element(By.CSS_SELECTOR, "option:checked").text
        self.assertEqual(default_selected_option, "Savings",
                         "Account type dropdown should be reset to default option")


    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
