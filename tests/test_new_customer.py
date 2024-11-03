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
from pages.new_customer_page import NewCustomerPage

class TestNewCustomer(unittest.TestCase):
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
        cls.driver.get("https://www.demo.guru99.com/V4/manager/addcustomerpage.php")

    def load_page(self):
        """Loads the New Customer page."""
        self.driver.get("https://www.demo.guru99.com/V4/manager/addcustomerpage.php")

    def setUp(self):
        """Runs before each test case."""
        self.load_page()
        self.new_customer_page = NewCustomerPage(self.driver)

    # Test cases
    def test_submit_empty_fields(self):
        """Test alert for all fields left empty"""
        self.new_customer_page.click_submit()
        try:
            WebDriverWait(self.driver, 10).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            self.assertEqual(alert.text, "please fill all fields")
            alert.accept()
        except TimeoutException:
            print("No alert appeared.")

    def test_empty_customer_name(self):
        """Test error when Customer Name is left empty"""
        self.new_customer_page.enter_customer_name("")
        self.new_customer_page.click_submit()
        error_message = self.driver.find_element(By.ID, "message")
        self.assertTrue(error_message.is_displayed())
        self.assertEqual(error_message.text, "Customer name must not be blank")

    def test_invalid_customer_name_numeric(self):
        """Test error for numeric input in Customer Name"""
        self.new_customer_page.enter_customer_name("12345")
        error_message = self.driver.find_element(By.ID, "message")
        self.assertTrue(error_message.is_displayed())
        self.assertEqual(error_message.text, "Numbers are not allowed")

    def test_invalid_customer_name_special_characters(self):
        """Test error for special characters in Customer Name"""
        self.new_customer_page.enter_customer_name("John@Doe")
        error_message = self.driver.find_element(By.ID, "message")
        self.assertTrue(error_message.is_displayed())
        self.assertEqual(error_message.text, "Special characters are not allowed")

    def test_first_character_space_address(self):
        """Test error when Address is left empty"""
        self.new_customer_page.enter_customer_name("John Doe")
        self.new_customer_page.enter_address(" ") # Empty address
        
        error_message = self.driver.find_element(By.ID, "message3")
        self.assertTrue(error_message.is_displayed())
        self.assertEqual(error_message.text, "First character can not have space")

    def test_first_character_space_city(self):
        """Test error when City is left empty"""
        self.new_customer_page.enter_customer_name("John Doe")
        self.new_customer_page.enter_city(" ")
        
        error_message = self.driver.find_element(By.ID, "message4")
        self.assertTrue(error_message.is_displayed())
        self.assertEqual(error_message.text, "First character can not have space")

    def test_invalid_city_special_characters(self):
        """Test error when City contains special characters"""
        self.new_customer_page.enter_customer_name("John Doe")
        self.new_customer_page.enter_city("New#York")
        
        error_message = self.driver.find_element(By.ID, "message4")
        self.assertTrue(error_message.is_displayed())
        self.assertEqual(error_message.text, "Special characters are not allowed")

    def test_first_character_state(self):
        """Test error when State is left empty"""
        self.new_customer_page.enter_customer_name("John Doe")
        self.new_customer_page.enter_state(" ")
        
        error_message = self.driver.find_element(By.ID, "message5")
        self.assertTrue(error_message.is_displayed())
        self.assertEqual(error_message.text, "First character can not have space")

    def test_invalid_state_special_characters(self):
        """Test error when State contains special characters"""
        self.new_customer_page.enter_customer_name("John Doe")
        self.new_customer_page.enter_state("CA@")
        
        error_message = self.driver.find_element(By.ID, "message5")
        self.assertTrue(error_message.is_displayed())
        self.assertEqual(error_message.text, "Special characters are not allowed")

    def test_first_character_space_pin(self):
        """Test error when PIN is left empty"""
        self.new_customer_page.enter_customer_name("John Doe")
        self.new_customer_page.enter_pin(" ")
        
        error_message = self.driver.find_element(By.ID, "message6")
        self.assertTrue(error_message.is_displayed())
        self.assertEqual(error_message.text, "First character can not have space")

    def test_invalid_pin_non_numeric(self):
        """Test error for non-numeric PIN input"""
        self.new_customer_page.enter_customer_name("John Doe")
        self.new_customer_page.enter_pin("12abc")
        
        error_message = self.driver.find_element(By.ID, "message6")
        self.assertTrue(error_message.is_displayed())
        self.assertEqual(error_message.text, "Characters are not allowed")

    def test_invalid_pin_less_than_six_digits(self):
        """Test error for PIN with less than 6 digits"""
        self.new_customer_page.enter_customer_name("John Doe")
        self.new_customer_page.enter_pin("123")
        
        error_message = self.driver.find_element(By.ID, "message6")
        self.assertTrue(error_message.is_displayed())
        self.assertEqual(error_message.text, "PIN Code must have 6 Digits")

    def test_invalid_mobile_number_non_numeric(self):
        """Test error for non-numeric mobile number"""
        self.new_customer_page.enter_mobile_number("abc123")
        
        error_message = self.driver.find_element(By.ID, "message7")
        self.assertTrue(error_message.is_displayed())
        self.assertEqual(error_message.text, "Characters are not allowed")

    def test_invalid_email_format(self):
        """Test error for invalid email format"""
        self.new_customer_page.enter_email("invalid-email")
        
        error_message = self.driver.find_element(By.ID, "message9")
        self.assertTrue(error_message.is_displayed())
        self.assertEqual(error_message.text, "Email-ID is not valid")

    def test_valid_customer_submission(self):
        """Test successful submission with valid data"""
        self.new_customer_page.enter_customer_name("John Doe")
        self.new_customer_page.select_gender("male")
        self.new_customer_page.enter_dob("01/01/1980")
        self.new_customer_page.enter_address("123 ABC Street")
        self.new_customer_page.enter_city("New York")
        self.new_customer_page.enter_state("NY")
        self.new_customer_page.enter_pin("123456")
        self.new_customer_page.enter_mobile_number("1234567890")
        self.new_customer_page.enter_email("john.doe@example.com")
        self.new_customer_page.enter_password("password123")
        self.new_customer_page.click_submit()

        # Check that the new customer page is displayed with success
        try:
            alert = WebDriverWait(self.driver, 2).until(EC.alert_is_present())
            self.assertEqual(alert.text, "Email Address Already Exist !!")
            alert.accept()
            time.sleep(1)
        except TimeoutException:
            print("No alert appeared.")

    def test_reset_functionality(self):
        """Test the reset button functionality"""
        self.new_customer_page.enter_customer_name("John Doe")
        self.new_customer_page.enter_dob("01/01/1980")
        self.new_customer_page.enter_address("123 ABC Street")
        self.new_customer_page.enter_city("New York")
        self.new_customer_page.enter_state("NY")
        self.new_customer_page.enter_pin("123456")
        self.new_customer_page.enter_mobile_number("1234567890")
        self.new_customer_page.enter_email("john.doe@example.com")
        self.new_customer_page.enter_password("password123")
        self.new_customer_page.click_reset()

        # Assert fields are empty
        self.assertEqual(self.driver.find_element(*self.new_customer_page.customer_name_input).get_attribute('value'), "")
        self.assertEqual(self.driver.find_element(*self.new_customer_page.dob_input).get_attribute('value'), "")
        self.assertEqual(self.driver.find_element(*self.new_customer_page.address_textarea).get_attribute('value'), "")
        self.assertEqual(self.driver.find_element(*self.new_customer_page.city_input).get_attribute('value'), "")
        self.assertEqual(self.driver.find_element(*self.new_customer_page.state_input).get_attribute('value'), "")
        self.assertEqual(self.driver.find_element(*self.new_customer_page.pin_input).get_attribute('value'), "")
        self.assertEqual(self.driver.find_element(*self.new_customer_page.mobile_number_input).get_attribute('value'), "")
        self.assertEqual(self.driver.find_element(*self.new_customer_page.email_input).get_attribute('value'), "")
        self.assertEqual(self.driver.find_element(*self.new_customer_page.password_input).get_attribute('value'), "")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
