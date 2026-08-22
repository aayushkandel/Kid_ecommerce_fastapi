import os
import uuid
import shutil
from fastapi import UploadFile, HTTPException


GALLERY_DIR = "gallery"


def upload_product_image(product_id: int,product_name: str,image: UploadFile):

    # Only allow JPEG and PNG
    allowed_types = {
        "image/jpeg": ".jpeg",
        "image/png": ".png",
        "image/jpg": ".jpg"
    }

    if image.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,detail="Only JPEG, PNG and JPG images are allowed")

    # Convert product name into folder-friendly name
    folder_name = product_name.replace(" ", "-").lower()

    # gallery/product_id/product_name
    product_folder = os.path.join(GALLERY_DIR,str(product_id),folder_name)

    # Create folder if it doesn't exist
    os.makedirs(product_folder,exist_ok=True)

    # Generate unique filename
    extension = allowed_types[image.content_type]

    filename = image.filename

    file_path = os.path.join(product_folder,filename)

    # Save image
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file,buffer)

    # Return path for database
    return file_path