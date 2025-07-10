import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

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
