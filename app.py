from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = os.getcwd() + '/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/upload", methods=['POST'])
def upload_image():
    """Upload and compresses image to local directory for future processing."""

    if 'file' not in request.files:
        print("File not in request")
        return redirect(url_for('index'))

    file = request.files['file']

    if file.filename == "":
        print("User did not select file")
        return redirect(url_for('index'))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('index'))


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.run(debug=True)
