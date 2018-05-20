"""Flask App"""

import os
from cropper import mat_to_buffer, crop, file_to_mat
from flask import Flask, redirect, request, send_file, render_template

app = Flask(__name__, static_url_path='/static')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


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

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == "__main__" :
    if os.getenv('FLASK_DEBUG') == '1':
        # Only for debugging while developing
        app.run(host='0.0.0.0', debug=True, port=80)
