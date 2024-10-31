# pages/logout_page.py

from selenium.webdriver.common.by import By

class LogoutPage:
    def __init__(self, driver):
        self.driver = driver
        self.logout_button = (By.LINK_TEXT, "Log out")

    def click_logout(self):
        """Clicks the logout button to log out of the account."""
        self.driver.find_element(*self.logout_button).click()

    def accept_logout_alert(self):
        """Accepts the alert that appears upon clicking logout."""
        alert = self.driver.switch_to.alert
        alert.accept()
