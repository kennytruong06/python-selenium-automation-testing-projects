from selenium.webdriver.common.by import By

class FundTransferPage:
    def __init__(self, driver):
        self.driver = driver
        self.payers_account_no_field = (By.NAME, "payersaccount")
        self.payees_account_no_field = (By.NAME, "payeeaccount")
        self.amount_field = (By.NAME, "ammount")
        self.description_field = (By.NAME, "desc")
        self.submit_button = (By.NAME, "AccSubmit")
        self.reset_button = (By.NAME, "res")

    def enter_payers_account_no(self, account_no):
        self.driver.find_element(*self.payers_account_no_field).send_keys(account_no)

    def enter_payees_account_no(self, account_no):
        self.driver.find_element(*self.payees_account_no_field).send_keys(account_no)

    def enter_amount(self, amount):
        self.driver.find_element(*self.amount_field).send_keys(amount)

    def enter_description(self, description):
        self.driver.find_element(*self.description_field).send_keys(description)

    def click_submit(self):
        self.driver.find_element(*self.submit_button).click()

    def click_reset(self):
        self.driver.find_element(*self.reset_button).click()