import unittest
import requests

class TestCreateActivityLive(unittest.TestCase):

    BASE_URL = "http://localhost:80"

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

# import unittest
# from app import create_app  # your factory function

# class TestCreateActivity(unittest.TestCase):
#     def setUp(self):
#         # create the app
#         self.app = create_app()
#         self.app.testing = True

#         # create a test client — stays in memory
#         self.client = self.app.test_client()

#     def test_host_activity_before_currentdate(self):
#         data = {
#             "activity_name": "Unit Test",
#             "activity_type": "Sports",
#             "skills_req": "Running",
#             "date": "2023-12-31T23:59",  # past date
#             "location": "Test Location",
#             "max_pax": 10
#         }

#         # Make an in-memory POST request
#         response = self.client.post(
#             "/host",
#             data=data,
#             follow_redirects=True
#         )

#         # Assertions
#         self.assertEqual(response.status_code, 200)
#         self.assertIn(b"Date cannot be in the past", response.data)

# if __name__ == '__main__':
#     unittest.main()
