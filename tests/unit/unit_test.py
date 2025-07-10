import os
import uuid

from werkzeug.utils import secure_filename

# def client():
#     app = create_app(testing=True)
#     app.config["TESTING"] = True
#     with app.test_client() as client:
#         yield client


# def test_host_activity_before_today(client):
#     response = client.post(
#         "/host",
#         data={
#             "activity_name": "Unit Test",
#             "activity_type": "Sports",
#             "skills_req": "Running",
#             "date": "2023-12-31T23:59",  # past date
#             "location": "Test Location",
#             "max_pax": 10,
#         },
#         follow_redirects=True,
#     )
#     assert response.status_code == 200
#     assert b"Date cannot be in the past" in response.data


# def test_create_feed_large_image(client):
#     image_path = "tests/assets/test_image2.jpg"
#     with open(image_path, "rb") as img:
#         data = {
#             "content": "Unit Test",
#             "image": (img, "test_image2.jpg"),  # file object and filename
#         }
#         response = client.post(
#             "/create",
#             data=data,
#             content_type="multipart/form-data",
#             follow_redirects=True,
#         )
#     print(response.data.decode())

#     assert response.status_code == 200

#     assert b"THis is just a radnom test lmaooo" in response.data



def testing_random_image_filename():
    image_filename_list = [
        "test.jpg", "test.jpg", "test.png",
        "test.png", "test.jpeg", "test.jpeg"
    ]
    unique_filenames = []

    for filename in image_filename_list:
        _, ext = os.path.splitext(secure_filename(filename))
        unique_filename = f"{uuid.uuid4().hex}{ext}"
        unique_filenames.append(unique_filename)

    # Uniqueness
    assert len(unique_filenames) == len(set(unique_filenames)), "Filenames are not unique"

    # Valid UUID
    for fname in unique_filenames:
        base, ext = os.path.splitext(fname)
        assert len(base) == 32, f"UUID length incorrect: {base}"
        assert all(c in "0123456789abcdef" for c in base), f"Invalid character in UUID: {base}"

    # Extension matches
    for fname, original in zip(unique_filenames, image_filename_list):
        _, orig_ext = os.path.splitext(original)
        _, ext = os.path.splitext(fname)
        assert ext == orig_ext, f"Extension mismatch: {ext} vs {orig_ext}"

    assert len(unique_filenames) == 5, "Expected 6 unique filenames, got {len(unique_filenames)}"
    
if __name__ == "__main__":
    testing_random_image_filename()
    print("All tests passed!")  # This will only run if the script is executed directly

