from io import BytesIO
from flask import Flask, redirect, request, send_file
from skimage import io
import cv2
import numpy as np

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

FACE_DETECTOR = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")

@app.route('/', methods=['POST'])
def upload_file():
    """Hande user uploading image"""
    # check if the post request has the file part
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']
    img = crop(io.imread(BytesIO(file)))

    return send_file(img)

def crop(img):
    """Crop to face"""
    image = cv2.imread(img)
    faces = detect(image)

    if len(faces) > 0:
        (x, y, w, h) = faces[0]
        image = image[y:y+h, x:x+w]

    return image

def detect(img):
    """Detect all faces in image"""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return FACE_DETECTOR.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.cv.CV_HAAR_SCALE_IMAGE
    )
