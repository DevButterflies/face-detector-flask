from deepface import DeepFace
from PIL import Image
import numpy as np

def detect_faces(image):
    """
    Extracts faces from an image using the MTCNN model in DeepFace.

    Args:
        image (numpy array): The input image.

    Returns:
        A list of PIL Image objects representing the cropped faces.
    """
    try:
        # Detect faces using the MTCNN model in DeepFace
        detected_faces = DeepFace.extract_faces(img_path=image, detector_backend='mtcnn', enforce_detection=False)

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
