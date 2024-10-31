from selenium.webdriver.common.by import By

class WithdrawPage:
    def __init__(self, driver):
        self.driver = driver
        self.account_number_field = (By.NAME, "accountno")
        self.amount_field = (By.NAME, "ammount")
        self.description_field = (By.NAME, "desc")
        self.submit_button = (By.NAME, "AccSubmit")
        self.reset_button = (By.NAME, "res")

    def enter_account_number(self, account_number):
        self.driver.find_element(*self.account_number_field).send_keys(account_number)

    def enter_amount(self, amount):
        self.driver.find_element(*self.amount_field).send_keys(amount)

    def enter_description(self, description):
        self.driver.find_element(*self.description_field).send_keys(description)

    def click_submit(self):
        self.driver.find_element(*self.submit_button).click()

    def click_reset(self):
        self.driver.find_element(*self.reset_button).click()