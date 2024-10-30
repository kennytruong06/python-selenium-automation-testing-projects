from selenium.webdriver.common.by import By

class AddAccountPage:
    def __init__(self, driver):
        self.driver = driver
        self.customer_id_field = (By.NAME, "cusid")
        self.account_type_dropdown = (By.NAME, "selaccount")
        self.initial_deposit_field = (By.NAME, "inideposit")
        self.submit_button = (By.NAME, "button2")
        self.reset_button = (By.NAME, "reset")

    def enter_customer_id(self, customer_id):
        self.driver.find_element(*self.customer_id_field).send_keys(customer_id)

    def select_account_type(self, account_type):
        dropdown = self.driver.find_element(*self.account_type_dropdown)
        for option in dropdown.find_elements(By.TAG_NAME, 'option'):
            if option.text == account_type:
                option.click()
                break

    def enter_initial_deposit(self, initial_deposit):
        self.driver.find_element(*self.initial_deposit_field).send_keys(initial_deposit)

    def click_submit(self):
        self.driver.find_element(*self.submit_button).click()

    def click_reset(self):
        self.driver.find_element(*self.reset_button).click()