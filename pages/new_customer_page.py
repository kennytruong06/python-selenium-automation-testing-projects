from selenium.webdriver.common.by import By

class NewCustomerPage:
    def __init__(self, driver):
        self.driver = driver
        self.customer_name_input = (By.NAME, "name")
        self.gender_radio_male = (By.XPATH, "//input[@value='m']")
        self.gender_radio_female = (By.XPATH, "//input[@value='f']")
        self.dob_input = (By.ID, "dob")
        self.address_textarea = (By.NAME, "addr")
        self.city_input = (By.NAME, "city")
        self.state_input = (By.NAME, "state")
        self.pin_input = (By.NAME, "pinno")
        self.mobile_number_input = (By.NAME, "telephoneno")
        self.email_input = (By.NAME, "emailid")
        self.password_input = (By.NAME, "password")
        self.submit_button = (By.NAME, "sub")
        self.reset_button = (By.NAME, "res")

    def enter_customer_name(self, name):
        self.driver.find_element(*self.customer_name_input).send_keys(name)

    def select_gender(self, gender):
        if gender.lower() == 'male':
            self.driver.find_element(*self.gender_radio_male).click()
        elif gender.lower() == 'female':
            self.driver.find_element(*self.gender_radio_female).click()

    def enter_dob(self, dob):
        self.driver.find_element(*self.dob_input).send_keys(dob)

    def enter_address(self, address):
        self.driver.find_element(*self.address_textarea).send_keys(address)

    def enter_city(self, city):
        self.driver.find_element(*self.city_input).send_keys(city)

    def enter_state(self, state):
        self.driver.find_element(*self.state_input).send_keys(state)

    def enter_pin(self, pin):
        self.driver.find_element(*self.pin_input).send_keys(pin)

    def enter_mobile_number(self, mobile_number):
        self.driver.find_element(*self.mobile_number_input).send_keys(mobile_number)

    def enter_email(self, email):
        self.driver.find_element(*self.email_input).send_keys(email)

    def enter_password(self, password):
        self.driver.find_element(*self.password_input).send_keys(password)

    def click_submit(self):
        self.driver.find_element(*self.submit_button).click()

    def click_reset(self):
        self.driver.find_element(*self.reset_button).click()
