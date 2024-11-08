# app/routes.py
from flask import Flask, request, jsonify, send_file
from app.services import opencv_service, ssd_service, mtcnn_service
from app.utils import decode_image, encode_image, crop_image, create_producer, create_consumer
from app import app
import io
import numpy as np
from PIL import Image
from threading import Thread
from config.config import KAFKA_INPUT_TOPIC, KAFKA_OUTPUT_TOPIC
import json as json
import base64
import cv2

producer = create_producer()
consumer = create_consumer()

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
    
# Kafka consumer function to handle messages
def consume_messages():
    while True:
        msg = consumer.poll(timeout=1.0)  # Poll Kafka broker
        if msg is None:
            continue
        if msg.error():
            print(f"Consumer error: {msg.error()}")
            continue

        # Deserialize input data (base64 encoded image from Kafka message)
        input_data = json.loads(msg.value().decode('utf-8'))
        input_image_b64 = input_data['input_image']

        # Decode the base64 image back into a numpy array
        input_image = base64.b64decode(input_image_b64)
        input_image_np = np.frombuffer(input_image, dtype=np.uint8)
        input_image = cv2.imdecode(input_image_np, cv2.IMREAD_COLOR)  # Decode image to OpenCV format

        # Process the image using one of your models (e.g., MTCNN)
        cropped_faces = mtcnn_service.detect_faces(input_image)  # Modify accordingly for SSD or OpenCV

        # Re-encode the cropped image back to base64
        if cropped_faces:
            # Assuming you use only the first cropped face
            cropped_image = cropped_faces[0]
            _, buffer = cv2.imencode('.jpg', cropped_image)
            cropped_image_b64 = base64.b64encode(buffer).decode('utf-8')

            # Prepare Kafka message with the cropped image
            output_data = {
                "input_image": input_image_b64,
                "cropped_image": cropped_image_b64,
                "model_used": "MTCNN",  # Or whatever model you used
                "metadata": {
                    "timestamp": "2024-10-29T12:00:00Z",
                    "request_id": input_data['metadata']['request_id']
                }
            }
            producer.produce(KAFKA_OUTPUT_TOPIC, value=json.dumps(output_data))
            producer.flush()  # Ensure message delivery

# Route to manually send an image to Kafka input topic
@app.route('/send_image', methods=['POST'])
def send_image():
    data = request.get_json()
    producer.produce(KAFKA_INPUT_TOPIC, value=json.dumps(data))
    producer.flush()
    return jsonify({"status": "Image sent to Kafka"}), 200