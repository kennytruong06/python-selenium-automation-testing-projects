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
from pages.new_customer_page import NewCustomerPage  # Đổi tên import thành DepositPage

class TestNewCustomer (unittest.TestCase):
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
        cls.driver.get("https://www.demo.guru99.com/V4/manager/addcustomerpage.php")

    def load_page(self):
        """Hàm này sẽ tải lại trang NewCustomer."""
        self.driver.get("https://www.demo.guru99.com/V4/manager/addcustomerpage.php")
        time.sleep(1)

    def setUp(self):
        """Hàm này sẽ chạy trước mỗi test case."""
        self.load_page()
        self.new_customer_page = NewCustomerPage(self.driver)
    def test_new_customer_successful(self):
    # Fill in the new customer details
        self.new_customer_page.enter_customer_name("John Doe")
        self.new_customer_page.select_gender("male")  # Assuming you have an option to specify gender
        self.new_customer_page.enter_date_of_birth("1990", "01", "01")  # Assuming date input method exists
        self.new_customer_page.enter_address("123 Elm Street")
        self.new_customer_page.enter_city("Springfield")
        self.new_customer_page.enter_state("Illinois")
        self.new_customer_page.enter_pin("123456")
        self.new_customer_page.enter_mobile("1234567890")
        self.new_customer_page.enter_email("johndoe@example.com")
        self.new_customer_page.enter_password("securePass123")

    # Click submit
        self.new_customer_page.click_submit()

    # Wait for success message or alert
        try:
            # Adjust the timeout as necessary for page load or alert appearance
            alert = WebDriverWait(self.driver, 2).until(EC.alert_is_present())
            self.assertEqual(alert.text, "Customer Registered Successfully")  # Use the actual expected success message
            alert.accept()
        except TimeoutException:
            # If no alert, check for success message on page instead
            success_message = self.driver.page_source
            self.assertIn("Customer Registered Successfully", success_message)  # Adjust based on the actual success text
            print("Customer registration was successful.")
        except Exception as e:
            print(f"An unexpected exception occurred: {e}")
            
    def test_customer_name_validations(self):
        """TC_001 - Verify Customer Name field validation messages."""
        self.new_customer_page.enter_customer_name("123")  # Numbers in name
        self.new_customer_page.click_submit()
        self.assertIn("Numbers are not allowed", self.driver.page_source)
        
        self.new_customer_page.enter_customer_name("")  # Blank name
        self.new_customer_page.click_submit()
        self.assertIn("Customer name must not be blank", self.driver.page_source)
        
        self.new_customer_page.enter_customer_name("John@")  # Special character
        self.new_customer_page.click_submit()
        self.assertIn("Special characters are not allowed", self.driver.page_source)
        
        self.new_customer_page.enter_customer_name(" John")  # Leading space
        self.new_customer_page.click_submit()
        self.assertIn("First character can not have space", self.driver.page_source)

    def test_address_validations(self):
        """TC_002 - Verify Address field validation messages."""
        self.new_customer_page.enter_address("")  # Blank address
        self.new_customer_page.click_submit()
        self.assertIn("Address Field must not be blank", self.driver.page_source)
        
        self.new_customer_page.enter_address(" @Home")  # Special character
        self.new_customer_page.click_submit()
        self.assertIn("Special characters are not allowed", self.driver.page_source)
        
        self.new_customer_page.enter_address(" Home")  # Leading space
        self.new_customer_page.click_submit()
        self.assertIn("First character can not have space", self.driver.page_source)

    def test_city_validations(self):
        """TC_003 - Verify City field validation messages."""
        self.new_customer_page.enter_city("")  # Blank city
        self.new_customer_page.click_submit()
        self.assertIn("City Field must not be blank", self.driver.page_source)
        
        self.new_customer_page.enter_city("New York1")  # Numbers in city
        self.new_customer_page.click_submit()
        self.assertIn("Numbers are not allowed", self.driver.page_source)
        
        self.new_customer_page.enter_city("New@York")  # Special character
        self.new_customer_page.click_submit()
        self.assertIn("Special characters are not allowed", self.driver.page_source)
        
        self.new_customer_page.enter_city(" New York")  # Leading space
        self.new_customer_page.click_submit()
        self.assertIn("First character can not have space", self.driver.page_source)

    def test_state_validations(self):
        """TC_004 - Verify State field validation messages."""
        self.new_customer_page.enter_state("")  # Blank state
        self.new_customer_page.click_submit()
        self.assertIn("State must not be blank", self.driver.page_source)
        
        self.new_customer_page.enter_state("California1")  # Numbers in state
        self.new_customer_page.click_submit()
        self.assertIn("Numbers are not allowed", self.driver.page_source)
        
        self.new_customer_page.enter_state("Cal@fornia")  # Special character
        self.new_customer_page.click_submit()
        self.assertIn("Special characters are not allowed", self.driver.page_source)
        
        self.new_customer_page.enter_state(" California")  # Leading space
        self.new_customer_page.click_submit()
        self.assertIn("First character can not have space", self.driver.page_source)

    def test_pin_validations(self):
        """TC_005 - Verify PIN field validation messages."""
        self.new_customer_page.enter_pin("abcd")  # Non-numeric characters
        self.new_customer_page.click_submit()
        self.assertIn("PIN Code must be numeric", self.driver.page_source)
        
        self.new_customer_page.enter_pin("1234")  # Less than required digits
        self.new_customer_page.click_submit()
        self.assertIn("PIN Code must have 6 Digits", self.driver.page_source)

    def test_mobile_number_validations(self):
        """TC_006 - Verify Mobile Number field validation messages."""
        self.new_customer_page.enter_mobile("abcd123")  # Alphanumeric
        self.new_customer_page.click_submit()
        self.assertIn("Mobile no must be numeric", self.driver.page_source)
        
        self.new_customer_page.enter_mobile(" 123456789")  # Leading space
        self.new_customer_page.click_submit()
        self.assertIn("First character can not have space", self.driver.page_source)

    def test_email_validations(self):
        """TC_007 - Verify Email field validation messages."""
        self.new_customer_page.enter_email("invalid_email")  # Invalid format
        self.new_customer_page.click_submit()
        self.assertIn("Email-ID is not valid", self.driver.page_source)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
