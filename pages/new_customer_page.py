from selenium.webdriver.common.by import By

class NewCustomerPage:
    def __init__(self, driver):
        self.driver = driver
        self.customer_name_field = (By.NAME, "name")
        self.gender_radio = {
            'male': (By.CSS_SELECTOR, "input[value='m']"),
            'female': (By.CSS_SELECTOR, "input[value='f']")
        }
        self.dob_field = (By.NAME, "dob")
        self.address_field = (By.NAME, "addr")
        self.city_field = (By.NAME, "city")
        self.state_field = (By.NAME, "state")
        self.pin_field = (By.NAME, "pinno")
        self.telephone_field = (By.NAME, "telephoneno")
        self.email_field = (By.NAME, "emailid")
        self.password_field = (By.NAME, "password")
        self.submit_button = (By.NAME, "sub")
        self.reset_button = (By.NAME, "res")

    def enter_customer_name(self, name):
        self.driver.find_element(*self.customer_name_field).send_keys(name)

    def select_gender(self, gender):
        # gender should be either 'male' or 'female'
        gender_radio_button = self.gender_radio.get(gender.lower())
        if gender_radio_button:
            self.driver.find_element(*gender_radio_button).click()

    def enter_dob(self, dob):
        self.driver.find_element(*self.dob_field).send_keys(dob)

    def enter_address(self, address):
        self.driver.find_element(*self.address_field).send_keys(address)

    def enter_city(self, city):
        self.driver.find_element(*self.city_field).send_keys(city)

    def enter_state(self, state):
        self.driver.find_element(*self.state_field).send_keys(state)

    def enter_pin(self, pin):
        self.driver.find_element(*self.pin_field).send_keys(pin)

    def enter_telephone(self, telephone):
        self.driver.find_element(*self.telephone_field).send_keys(telephone)

    def enter_email(self, email):
        self.driver.find_element(*self.email_field).send_keys(email)

    def enter_password(self, password):
        self.driver.find_element(*self.password_field).send_keys(password)

    def click_submit(self):
        self.driver.find_element(*self.submit_button).click()

    def click_reset(self):
        self.driver.find_element(*self.reset_button).click()
