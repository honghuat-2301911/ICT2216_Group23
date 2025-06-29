import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

class RegisterTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        service = Service(ChromeDriverManager().install())
        cls.driver = webdriver.Chrome(service=service, options=options)
        cls.driver.implicitly_wait(10)

    def test_title(self):
        self.driver.get("https://example.com")
        self.assertIn("Example Domain", self.driver.title)

    def test_paragraph_text(self):
        self.driver.get("https://example.com")
        paragraph = self.driver.find_element(By.TAG_NAME, "p")
        self.assertIn("illustrative examples", paragraph.text)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
