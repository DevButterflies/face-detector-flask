import cv2

def detect_faces(image):
    """
    Detects faces in an image using OpenCV's Haar Cascade classifier.

    Args:
        image: The input image.

    Returns:
        A list of bounding boxes for detected faces.
    """
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    if len(faces) > 0:  # Check if any faces were detected
        return faces
    else:
        return []  # Return an empty list if no faces are found