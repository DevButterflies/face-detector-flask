from deepface import DeepFace
from PIL import Image
import numpy as np
import cv2

def detect_faces(image):
    """
    Extracts faces from an image file using the SSD model in DeepFace.

    Args:
        image_file: The image file object.

    Returns:
        A list of PIL Image objects representing the cropped faces.
    """
    try:
        # Convert the image to OpenCV format if needed (ensure it's a numpy array)
        if not isinstance(image, np.ndarray):
            print("Input image must be a numpy array.")
            return []

        # Convert numpy array to OpenCV BGR format if it's not
        if len(image.shape) == 3 and image.shape[2] == 3:
            image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        else:
            image_bgr = image

        # Detect faces using the SSD model in DeepFace
        detected_faces = DeepFace.extract_faces(img_path=image_bgr, detector_backend='ssd', enforce_detection=False)

        cropped_faces = []

        # If faces are detected
        if detected_faces:
            for face_data in detected_faces:
                # Get the bounding box coordinates from the 'facial_area' key
                region = face_data.get('facial_area')
                if region:
                    x, y, w, h = region['x'], region['y'], region['w'], region['h']

                    # Crop the face from the original image using the bounding box
                    cropped_face = image[y:y+h, x:x+w]

                    # Convert the cropped face (numpy array) to a PIL Image
                    cropped_face_pil = Image.fromarray(cropped_face.astype(np.uint8))

                    # Append the cropped PIL Image to the list
                    cropped_faces.append(cropped_face_pil)

        return cropped_faces

    except Exception as e:
        print(f"Error occurred during face detection: {e}")
        return []