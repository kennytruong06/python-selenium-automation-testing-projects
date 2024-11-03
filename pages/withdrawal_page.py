from selenium.webdriver.common.by import By

class WithdrawalPage:
    def __init__(self, driver):
        self.driver = driver
        self.account_no_input = (By.NAME, "accountno")
        self.amount_input = (By.NAME, "ammount")
        self.description_input = (By.NAME, "desc")
        self.submit_button = (By.NAME, "AccSubmit")
        self.reset_button = (By.NAME, "res")

    def enter_account_no(self, account_no):
        """Enter account number."""
        account_no_field = self.driver.find_element(*self.account_no_input)
        account_no_field.clear()
        account_no_field.send_keys(account_no)

    def enter_amount(self, amount):
        """Enter amount."""
        amount_field = self.driver.find_element(*self.amount_input)
        amount_field.clear()
        amount_field.send_keys(amount)

    def enter_description(self, description):
        """Enter description."""
        description_field = self.driver.find_element(*self.description_input)
        description_field.clear()
        description_field.send_keys(description)

    def click_submit(self):
        """Click the submit button."""
        submit_button = self.driver.find_element(*self.submit_button)
        submit_button.click()

    def click_reset(self):
        """Click the reset button to clear all fields."""
        reset_button = self.driver.find_element(*self.reset_button)
        reset_button.click()
