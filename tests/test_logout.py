# tests/test_logout.py

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
from pages.logout_page import LogoutPage

class TestLogout(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.get("https://www.demo.guru99.com/V4/")
        cls.driver.implicitly_wait(10)

        # Login before testing logout
        login_page = LoginPage(cls.driver)
        login_page.enter_username("mngr599682")  # Change this to your username
        login_page.enter_password("nyqEreh")  # Change this to your password
        login_page.click_login()

    def setUp(self):
        """Runs before each test case."""
        self.logout_page = LogoutPage(self.driver)

    def test_logout(self):
        """Tests the logout functionality."""
        # Click the logout button
        self.logout_page.click_logout()

        # Handle alert confirmation
        try:
            WebDriverWait(self.driver, 2).until(EC.alert_is_present())
            self.logout_page.accept_logout_alert()
            time.sleep(1)
        except TimeoutException:
            self.fail("Logout alert did not appear as expected.")

        # Check if redirected to the login page
        login_text = self.driver.find_element(By.XPATH, "//h2[contains(text(),'Guru99 Bank')]").text
        self.assertIn("Guru99 Bank", login_text, "Logout failed; not redirected to login page")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
