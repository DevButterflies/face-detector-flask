# app/routes.py
from flask import Flask, request, jsonify, send_file
from app.services import opencv_service, ssd_service, mtcnn_service
from app.utils import decode_image, crop_image
from app import app
import io
import numpy as np
from PIL import Image
import json as json




@app.route('/detect/opencv', methods=['POST'])
def detect_face_opencv():
    """
    Detects faces in an uploaded image using OpenCV.

    Args:
        image (file): The image file to process.

    Returns:
        The cropped face image or an error message.
    """
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    image_file = request.files['image']

    try:
        image = decode_image(image_file)
        faces = opencv_service.detect_faces(image)

        cropped_images = []
        if len(faces) > 0:  # Check if any faces were detected
            for (x, y, w, h) in faces:  # Correctly unpack the bounding box
                cropped_image = crop_image(image, [x, y, w, h])

                # Convert to PIL Image
                img = Image.fromarray(cropped_image.astype(np.uint8))

                # Create an in-memory byte stream
                img_io = io.BytesIO()
                img.save(img_io, 'JPEG', quality=90)
                img_io.seek(0)

                cropped_images.append(send_file(img_io, mimetype='image/jpeg'))

            return cropped_images[0]  # Return the first cropped image

        else:
            return jsonify({'error': 'No faces detected'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/detect/ssd', methods=['POST'])
def detect_face_ssd():
    """
    Detects faces in an uploaded image using ssd.

    Args:
        image (file): The image file to process.

    Returns:
        The first cropped face image as a JPEG, or an error message.
    """
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    image_file = request.files['image']

    try:
        # Decode the image into a numpy array
        image = decode_image(image_file)

        # Call the MTCNN service to detect and crop faces
        faces = ssd_service.detect_faces(image)

        if faces:
            # Get the first cropped face (PIL Image)
            cropped_image = faces[0]

            # Create an in-memory byte stream
            img_io = io.BytesIO()
            cropped_image.save(img_io, 'JPEG', quality=90)  # Save the PIL Image to the stream
            img_io.seek(0)  # Reset the stream position to the beginning

            # Return the cropped image as a response
            return send_file(img_io, mimetype='image/jpeg')

        else:
            return jsonify({'error': 'No faces detected'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/detect/mtcnn', methods=['POST'])
def detect_face_mtcnn():
    """
    Detects faces in an uploaded image using MTCNN.

    Args:
        image (file): The image file to process.

    Returns:
        The first cropped face image as a JPEG, or an error message.
    """
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    image_file = request.files['image']

    try:
        # Decode the image into a numpy array
        image = decode_image(image_file)

        # Call the MTCNN service to detect and crop faces
        faces = mtcnn_service.detect_faces(image)

        if faces:
            # Get the first cropped face (PIL Image)
            cropped_image = faces[0]

            # Create an in-memory byte stream
            img_io = io.BytesIO()
            cropped_image.save(img_io, 'JPEG', quality=90)  # Save the PIL Image to the stream
            img_io.seek(0)  # Reset the stream position to the beginning

            # Return the cropped image as a response
            return send_file(img_io, mimetype='image/jpeg')

        else:
            return jsonify({'error': 'No faces detected'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
