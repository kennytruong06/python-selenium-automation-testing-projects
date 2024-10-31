# pages/customised_page.py
from selenium.webdriver.common.by import By

class CustomisedPage:
    def __init__(self, driver):
        self.driver = driver
        # Define locators for the elements on the page
        self.account_no_input = (By.NAME, "accountno")
        self.from_date_input = (By.NAME, "fdate")
        self.to_date_input = (By.NAME, "tdate")
        self.min_transaction_value_input = (By.NAME, "amountlowerlimit")
        self.num_transaction_input = (By.NAME, "numtransaction")
        self.submit_button = (By.NAME, "AccSubmit")
        self.reset_button = (By.NAME, "res")

    def enter_account_no(self, account_no):
        self.driver.find_element(*self.account_no_input).send_keys(account_no)

    def enter_from_date(self, from_date):
        self.driver.find_element(*self.from_date_input).send_keys(from_date)

    def enter_to_date(self, to_date):
        self.driver.find_element(*self.to_date_input).send_keys(to_date)

    def enter_min_transaction_value(self, min_value):
        self.driver.find_element(*self.min_transaction_value_input).send_keys(min_value)

    def enter_num_transaction(self, num_transaction):
        self.driver.find_element(*self.num_transaction_input).send_keys(num_transaction)

    def click_submit(self):
        self.driver.find_element(*self.submit_button).click()

    def click_reset(self):
        self.driver.find_element(*self.reset_button).click()
