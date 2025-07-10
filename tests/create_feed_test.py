import os
import time
import unittest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class CreateFeedPageTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        options = Options()
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--allow-insecure-localhost")
        options.add_argument("--headless")  # for CI
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        cls.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        )
        cls.driver.implicitly_wait(10)
        cls.base_url = "https://localhost"  # adjust if needed

        cls.seeded_email = "2301875@sit.singaporetech.edu.sg"
        cls.seeded_password = "123123123"

    def fill_login_form(self, email, password):
        self.driver.get(f"{self.base_url}/login")
        print(self.driver.current_url)
        print(self.driver.page_source)  # debug
        self.driver.find_element(By.NAME, "email").send_keys(email)
        self.driver.find_element(By.NAME, "password").send_keys(password)
        self.driver.find_element(By.CLASS_NAME, "login-btn").click()
        time.sleep(2)

    def fill_feed_form(self, content_text, image_path):
        # go to the feed creation page
        self.driver.get(f"{self.base_url}/feed")
        print(self.driver.current_url)
        print(self.driver.page_source)  # debug
        wait = WebDriverWait(self.driver, 10)

        # wait for and fill content
        content_field = wait.until(EC.element_to_be_clickable((By.NAME, "content")))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", content_field)
        content_field.clear()
        content_field.send_keys(content_text)

        # wait for and upload image
        image_input = wait.until(EC.presence_of_element_located((By.NAME, "image")))
        image_input.send_keys(image_path)

        # wait for and click submit button
        submit_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        submit_btn.click()

        # optional: wait until the page shows confirmation or content
        time.sleep(2)


    def test_create_feed(self):
        try:
            # login first
            self.fill_login_form(self.seeded_email, self.seeded_password)
            self.assertIn("Bulletin Board", self.driver.page_source)  # adjust expected page

            # create feed
            test_image = os.path.abspath("tests/assets/test_image1.jpg")  # make sure this file exists!
            self.fill_feed_form("This is a Selenium feed test", test_image)

            # check that feed was created
            self.assertIn("This is a Selenium feed test", self.driver.page_source)

            # logout
            self.driver.get(f"{self.base_url}/logout")

        except Exception:
            os.makedirs("artifacts", exist_ok=True)
            self.driver.save_screenshot("artifacts/create_feed_failure.png")
            with open("artifacts/create_feed_debug.html", "w", encoding="utf-8") as f:
                f.write(self.driver.page_source)
            raise

    def test_create_feed_large_image(self):
        """
        Try to create a feed with an image >1MB
        Expect to see a validation error.
        """
        try:
            # login
            self.fill_login_form(self.seeded_email, self.seeded_password)
            self.assertIn("Bulletin Board", self.driver.page_source)  # adjust expected page

            # create feed
            test_image = os.path.abspath("tests/assets/test_image2.jpg")  # make sure this file exists!
            self.fill_feed_form("This is a failed Selenium feed test", test_image)

            wait = WebDriverWait(self.driver, 10)
            error_elem = wait.until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, "#flashModal .flash-message.error")
                )
            )
            self.assertIn("Image size must be less than 1MB.", error_elem.text)

            # logout to clean up
            self.driver.get(f"{self.base_url}/logout")

        except Exception:
            os.makedirs("artifacts", exist_ok=True)
            self.driver.save_screenshot("artifacts/create_feed_large_image_failure.png")
            with open("artifacts/create_feed_large_image_debug.html", "w", encoding="utf-8") as f:
                f.write(self.driver.page_source)
            raise


    # def test_create_activity_success(self):
    #     try:
    #         # Assert that the login with the seeded email and password is successful
    #         # After login, the user should be redirected to the bulletin board page
    #         self.fill_login_form(email=self.seeded_email, password=self.seeded_password)
    #         self.assertIn("Bulletin Board", self.driver.page_source)

    #         # Open the host activity modal
    #         host_button = self.driver.find_element(
    #             By.XPATH, "//button[contains(text(), 'Host Activity')]"
    #         )
    #         host_button.click()
    #         time.sleep(1)  # Wait for modal animation

    #         self.fill_activity_form(
    #             name="Selenium Test Activity", date="3000-07-08T15:30"
    #         )

    #         # Assert that the activity was created successfully
    #         self.assertIn("Selenium Test Activity", self.driver.page_source)

    #         # Logout to reset the state for the next test
    #         self.driver.get(f"{self.base_url}/logout")

    #     except Exception as e:
    #         os.makedirs("artifacts", exist_ok=True)
    #         self.driver.save_screenshot("artifacts/create_activity_success.png")
    #         with open("artifacts/debug.html", "w", encoding="utf-8") as f:
    #             f.write(self.driver.page_source)
    #         raise  # Re-raise so the test still fails

    # def test_create_activity_past_date(self):
    #     try:
    #         # Assert that the login with the seeded email and password is successful
    #         # After login, the user should be redirected to the bulletin board page
    #         self.fill_login_form(email=self.seeded_email, password=self.seeded_password)
    #         self.assertIn("Bulletin Board", self.driver.page_source)

    #         # Open the host activity modal
    #         host_button = self.driver.find_element(
    #             By.XPATH, "//button[contains(text(), 'Host Activity')]"
    #         )
    #         host_button.click()
    #         time.sleep(1)  # Wait for modal animation

    #         self.fill_activity_form(
    #             name="Past Date Activity",
    #             date="2000-07-08T15:30",  # Past date for testing failure
    #         )

    #         wait = WebDriverWait(self.driver, 10)
    #         error_elem = wait.until(
    #             EC.visibility_of_element_located(
    #                 (By.CSS_SELECTOR, "#flashModal .flash-message.error")
    #             )
    #         )
    #         self.assertIn("Date cannot be in the past", error_elem.text)

    #         # Logout to reset the state for the next test
    #         self.driver.get(f"{self.base_url}/logout")

    #     except Exception as e:
    #         os.makedirs("artifacts", exist_ok=True)
    #         self.driver.save_screenshot("artifacts/create_activity_success.png")
    #         with open("artifacts/debug.html", "w", encoding="utf-8") as f:
    #             f.write(self.driver.page_source)
    #         raise  # Re-raise so the test still fails

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()
