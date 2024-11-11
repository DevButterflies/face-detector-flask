# app/utils.py
import cv2
import base64
import numpy as np

def decode_image(image_file):
    """
    Decodes an image file to a NumPy array.

    Args:
        image_file: The image file object.

    Returns:
        A NumPy array representing the image.
    """
    image_file.seek(0)
    file_bytes = np.asarray(bytearray(image_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    return image

def encode_image(image):
    """
    Encodes a NumPy array image to a base64 string.

    Args:
        image: The image as a NumPy array.

    Returns:
        A base64 encoded string representing the image.
    """
    _, buffer = cv2.imencode('.jpg', image)
    jpg_as_text = base64.b64encode(buffer).decode('utf-8')
    return jpg_as_text

def crop_image(image, box):
    """
    Crops a face from an image based on a bounding box.

    Args:
        image: The input image.
        box: A list or tuple [x, y, w, h] representing the bounding box.

    Returns:
        The cropped image.
    """
    x, y, w, h = box
    return image[y:y+h, x:x+w]

