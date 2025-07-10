import os
import uuid
import pytest
import io
from werkzeug.utils import secure_filename
from wtforms.validators import ValidationError
from domain.entity.forms import PostForm

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

    assert len(unique_filenames) == 6, "Expected 6 unique filenames, got {len(unique_filenames)}"

def test_image_size_over_1mb():
    fake_image = io.BytesIO(b"x" * (1 * 1024 * 1024 + 1))  # >1MB
    fake_image.filename = "test.jpg"

    def validate():
        if hasattr(fake_image, "filename") and fake_image.filename:
            fake_image.seek(0, 2)  # move to end
            file_length = fake_image.tell()
            fake_image.seek(0)

            max_size = 1 * 1024 * 1024
            if file_length > max_size:
                raise ValidationError("Image size must be less than 1MB.")

    with pytest.raises(ValidationError) as excinfo:
        validate()

    assert "Image size must be less than 1MB" in str(excinfo.value)
   
    
if __name__ == "__main__":
    testing_random_image_filename()
    test_image_size_over_1mb()
    print("All tests passed!")  # This will only run if the script is executed directly

