import unittest
import sys
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# from data_source.user_queries import clear_users

class RegisterPageTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        cls.driver.implicitly_wait(10)
        cls.base_url = "http://localhost"
        cls.test_email = "testuser@example.com"  # Same email to test duplicate

        # clear_users()  # Clear users before tests to ensure a clean state

    def fill_registration_form(self, email):
        self.driver.get(f"{self.base_url}/register")
        self.driver.find_element(By.NAME, "name").send_keys("Test User")
        self.driver.find_element(By.NAME, "email").send_keys(email)
        self.driver.find_element(By.NAME, "password").send_keys("securepassword")
        self.driver.find_element(By.NAME, "confirm_password").send_keys("securepassword")
        self.driver.find_element(By.NAME, "skill_lvl").send_keys("Intermediate")
        self.driver.find_element(By.NAME, "sports_exp").send_keys("Played soccer for 3 years")
        self.driver.find_element(By.CLASS_NAME, "register-btn").click()
        time.sleep(2)

    def test_register_success(self):
        self.fill_registration_form(email=self.test_email)
        self.assertIn("Registration successful", self.driver.page_source)

    def test_register_duplicate_email(self):
        self.fill_registration_form(email=self.test_email)
        self.assertIn("Something went wrong. Please try again.", self.driver.page_source)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
