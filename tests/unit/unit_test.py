import pytest
from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_host_activity_before_today(client):
    response = client.post('/host', data={
        "activity_name": "Unit Test",
        "activity_type": "Sports",
        "skills_req": "Running",
        "date": "2023-12-31T23:59",  # past date
        "location": "Test Location",
        "max_pax": 10
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Date cannot be in the past" in response.data
    
def test_create_feed_large_image(client):
    image_path = "tests/assets/test_image2.jpg"
    with open(image_path, 'rb') as img:
        data = {
            "content": "Unit Test",
            "image": (img, "test_image2.jpg")  # file object and filename
        }
        response = client.post(
            '/create', 
            data=data,
            content_type='multipart/form-data', 
            follow_redirects=True
        )

    assert response.status_code == 200
    assert b"xx" in response.data

