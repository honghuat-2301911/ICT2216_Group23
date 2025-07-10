import unittest
from app import create_app  
from flask import url_for
from domain.control import bulletin_management

class TestCreateActivity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app = create_app()
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['TESTING'] = True
        cls.client = app.test_client()


    def test_host_activity_before_currentdate(self):
        data = {
            "activity_name": "Unit Test",
            "activity_type": "Sports",
            "skills_req": "Running",
            "date": "2023-12-31T23:59",  # old date
            "location": "Test Location",
            "max_pax": 10
        }
        response = self.client.post(
            "/host", 
            data=data, 
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Host form error: Date cannot be in the past", response.data)

if __name__ == '__main__':
    unittest.main()
