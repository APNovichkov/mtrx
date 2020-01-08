from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
from PIL import Image

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
        output_filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(output_filepath)

        compress_file(output_filepath)

        return redirect(url_for('index'))

def compress_file(filepath):
    """Compress input file and replace it with compressed version in jpg format."""
    # Open input file
    foo = Image.open(filepath)
    foo = foo.resize((int(foo.size[0] / 3), int(foo.size[1] / 3)), Image.ANTIALIAS)

    # Remove old file
    if os.path.exists(filepath):
        os.remove(filepath)
    else:
        print("The file: {} does not exist".format(filepath))

    # Save new file
    raw_filepath = filepath.split('.')[0]
    foo.save(raw_filepath + ".jpg", quality=75)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.run(debug=True)
