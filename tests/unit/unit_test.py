import unittest
import requests

class TestCreateActivityLive(unittest.TestCase):

    BASE_URL = "http://localhost:8000"

    def test_host_activity_before_currentdate(self):
        data = {
            "activity_name": "Unit Test",
            "activity_type": "Sports",
            "skills_req": "Running",
            "date": "2023-12-31T23:59",  # old date
            "location": "Test Location",
            "max_pax": 10
        }

        # POST to the running Flask app in Docker
        response = requests.post(
            f"{self.BASE_URL}/host",
            data=data
        )

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertIn("Date cannot be in the past", response.text)

if __name__ == '__main__':
    unittest.main()
