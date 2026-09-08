import os
import shutil
from fastapi import UploadFile, HTTPException


GALLERY_DIR = "gallery"


def upload_product_image(
    product_id: int,
    product_name: str,
    image: UploadFile
):

    allowed_extensions = {".jpg", ".jpeg", ".png"}

    # Get extension from filename
    extension = os.path.splitext(image.filename)[1].lower()

    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Only JPEG, PNG and JPG images are allowed"
        )

    # Convert product name into folder-friendly name
    folder_name = product_name.replace(" ", "-").lower()

    # gallery/product_id/product_name
    product_folder = os.path.join(
        GALLERY_DIR,
        str(product_id),
        folder_name
    )

    # Create folder
    os.makedirs(product_folder, exist_ok=True)

    # Generate unique filename
    filename = image.filename

    file_path = os.path.join(
        product_folder,
        filename
    )

    # Save image
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    # Return path
    return file_path