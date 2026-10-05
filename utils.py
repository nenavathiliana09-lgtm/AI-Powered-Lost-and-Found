import os
import uuid
from PIL import Image


def save_uploaded_image(uploaded_file, folder):
    os.makedirs(folder, exist_ok=True)

    file_name = f"{uuid.uuid4().hex}.jpg"
    file_path = os.path.join(folder, file_name)

    image = Image.open(uploaded_file).convert("RGB")
    image.save(file_path)

    return file_path


def validate_image(uploaded_file):
    try:
        image = Image.open(uploaded_file)
        image.verify()
        return True
    except Exception:
        return False