"""Test Computer Vision"""

import cv2
from context import cropper

def test_detector():
    im = cv2.imread("tests/test_img.jpg")
    faces = cropper.detect(im)
    assert len(faces) > 0
