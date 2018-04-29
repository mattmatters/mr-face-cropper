import os
from io import BytesIO
from flask import Flask, redirect, request, send_file, render_template
from skimage import io
import cv2
import numpy as np

app = Flask(__name__, static_url_path='/static')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
FACE_DETECTOR = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")

@app.route('/')
def index():
    """Main page"""
    return render_template('landing.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Hande user uploading image"""
    # check if the post request has the file part
    if 'photo' not in request.files:
        return redirect(request.url)

    file = request.files['photo']
    extension = file.filename.rsplit('.', 1)[1].lower()

    if not allowed_file(file.filename):
        return redirect(request.url)

    img = crop(file_to_mat(file))
    ret_file = mat_to_buffer(img, extension)

    return send_file(ret_file, attachment_filename=file.filename)

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

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == "__main__" :
    if os.getenv('FLASK_DEBUG') == '1':
        # Only for debugging while developing
        app.run(host='0.0.0.0', debug=True, port=80)
