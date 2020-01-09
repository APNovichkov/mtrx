from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
from PIL import Image

UPLOAD_FOLDER = 'static/uploads'
UPLOAD_FOLDER_FULL = os.path.join(os.getcwd(), UPLOAD_FOLDER)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER_FULL

# Route Functions

@app.route("/")
def welcome():
    """Show the welcome page."""

    print("This is the full upload path: {}".format(UPLOAD_FOLDER_FULL))

    return render_template('index.html')

@app.route("/dashboard/<filename>")
def show_dashboard(filename):
    """Shows the dashboard from which all further actions are taken."""

    filepath = "/" + os.path.join(UPLOAD_FOLDER, filename)

    return render_template("dashboard.html", filename=filename, filepath=filepath)

@app.route("/generate-image/<filename>", methods=['POST'])
def generate_image(filename):
    print("Need to apply filter and generate new image from this file: {}".format(filename))

    rows = 3
    columns = 3

    items = []

    print("Args in request: {}".format(request.form))

    return redirect(url_for('show_dashboard', filename=filename))


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
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        filename = compress_file(filename)

        return redirect(url_for('show_dashboard', filename=filename))

# Helper Functions

def compress_file(filename):
    """Compress input file and replace it with compressed version in jpg format."""

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    # Open input file
    foo = Image.open(filepath)
    foo = foo.resize((int(foo.size[0] / 3), int(foo.size[1] / 3)), Image.ANTIALIAS)

    # Remove old file
    if os.path.exists(filepath):
        os.remove(filepath)
    else:
        print("The file: {} does not exist".format(filepath))

    # Save new file
    jpg_filename = filename.split('.')[0] + '.jpg'
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], jpg_filename)
    foo.save(filepath, quality=75)

    return jpg_filename

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.run(debug=True)
