import os
import sys
import time
import unittest
import random
import string

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


class RegisterPageTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        options = Options()
        options.add_argument('--ignore-certificate-errors')  # <-- key line
        options.add_argument('--allow-insecure-localhost')   # optional, but useful
        options.add_argument('--headless')                   # for CI
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        cls.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        )
        cls.driver.implicitly_wait(10)
        cls.base_url = "https://localhost"

        # register a test user to test login functionality
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        cls.test_email = f"{random_suffix}@example.com"
        cls.base_password = "securepassword"
        cls.fill_registration_form(email=cls.test_email, password=cls.base_password)


    def fill_registration_form(self, email, password):
        self.driver.get(f"{self.base_url}/register")
        self.driver.find_element(By.NAME, "name").send_keys("Test User")
        self.driver.find_element(By.NAME, "email").send_keys(email)
        self.driver.find_element(By.NAME, "password").send_keys(password)
        self.driver.find_element(By.NAME, "confirm_password").send_keys(password)
        self.driver.find_element(By.CLASS_NAME, "register-btn").click()
        time.sleep(2)

    def fill_login_form(self):
        self.driver.get(f"{self.base_url}/login")
        self.driver.find_element(By.NAME, "email").send_keys(self.test_email)
        self.driver.find_element(By.NAME, "password").send_keys(self.base_password)
        self.driver.find_element(By.CLASS_NAME, "login-btn").click()
        time.sleep(2)

    def test_login_success(self):
        try:
            self.fill_registration_form(email=self.test_email, password=self.base_password)
            self.assertIn("You must verify your email before logging in. Please check your inbox.", self.driver.page_source)

        except Exception as e:
            os.makedirs("artifacts", exist_ok=True)
            self.driver.save_screenshot("artifacts/register_success.png")
            with open("artifacts/debug.html", "w", encoding="utf-8") as f:
                f.write(self.driver.page_source)
            raise  # Re-raise so the test still fails


    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()
