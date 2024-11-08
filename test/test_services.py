import unittest
import cv2
from PIL import Image
import numpy as np
from face_detector_service.app.services import opencv_service, ssd_service, mtcnn_service



class TestFaceDetectionServices(unittest.TestCase):

    def setUp(self):
        # Load a test image that contains multiple faces for testing
        self.image_path = "tests/test1.jpg"  # Replace with a valid test image path
        self.image_cv2 = cv2.imread(self.image_path)
        self.image_pil = Image.open(self.image_path)
    
    def test_opencv_service(self):
        # Test OpenCV face detection service
        faces = opencv_service.detect_faces(self.image_cv2)
        self.assertGreater(len(faces), 0, "No faces detected using OpenCV service.")
    
    def test_ssd_service(self):
        # Test SSD face detection service
        faces = ssd_service.detect_faces(self.image_pil)
        self.assertGreater(len(faces), 0, "No faces detected using SSD service.")
    
    def test_mtcnn_service(self):
        # Test MTCNN face detection service
        faces = mtcnn_service.detect_faces(self.image_pil)
        self.assertGreater(len(faces), 0, "No faces detected using MTCNN service.")

if __name__ == '__main__':
    unittest.main()
