import sys
import os

# Thêm thư mục gốc của dự án vào sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from selenium import webdriver
from pages.login_page import LoginPage


class TestLogin(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://www.demo.guru99.com/V4/")

    def test_login_successful(self):
        login_page = LoginPage(self.driver)
        login_page.enter_username("mngr599682")
        login_page.enter_password("nyqEreh")
        login_page.click_login()

        self.assertIn("Guru99 Bank Manager HomePage", self.driver.title)

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
