"""Computer Vision"""

from io import BytesIO
from skimage import io
import cv2
import numpy as np

FACE_DETECTOR = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")

def mat_to_buffer(mat, extension):
    """Encode opencv type to byte stream"""
    ret_file = BytesIO()
    _, buf = cv2.imencode('.'+extension, mat)

    ret_file.write(buf.tostring())
    ret_file.seek(0)

    return ret_file

def file_to_mat(file):
    buffer = BytesIO()
    file.save(buffer)
    buffer.seek(0)
    mat = cv2.cvtColor(io.imread(buffer), cv2.COLOR_BGR2RGB)

    return mat

def crop(img):
    """Crop to face"""
#    image = cv2.imread(img)
    faces = detect(img)

    if len(faces) > 0:
        (x, y, w, h) = faces[0]
        img = img[y:y+h, x:x+w]

    return img

def detect(img):
    """Detect all faces in image"""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return FACE_DETECTOR.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )
