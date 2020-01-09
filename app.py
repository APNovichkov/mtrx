from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
from PIL import Image
import filtering

UPLOAD_FOLDER = '/static/uploads'
UPLOAD_FOLDER_FULL = os.getcwd() + UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER_FULL

# Route Functions

@app.route("/")
def welcome():
    """Show the welcome page."""

    print("This is the full upload path: {}".format(UPLOAD_FOLDER_FULL))

    return render_template('index.html')

@app.route("/dashboard/<original_filename>/<edited_filename>")
def show_dashboard(original_filename, edited_filename):
    """Shows the dashboard from which all further actions are taken."""

    original_filepath = os.path.join(UPLOAD_FOLDER, original_filename)
    edited_filepath = os.path.join(UPLOAD_FOLDER, edited_filename)

    return render_template("dashboard.html", original_filepath=original_filepath, edited_filepath=edited_filepath)

@app.route("/generate-image/<original_filename>", methods=['POST'])
def generate_image(original_filename):
    print("Need to apply filter and generate new image from this file: {}".format(filename))

    # Define size of convolution matrix
    rows = 3
    columns = 3

    # Get filter from input user data
    filter = get_matrix_from_form_data(request.form, rows)
    print("This is the user inputted filter: {}".format(filter))


    filepath = get_upload_filepath_from_filename(original_filename)

    edited_filename = filtering.apply_filter(filepath, filter)

    return redirect(url_for('show_dashboard', original_filename=filename, edited_filename=edited_filename))


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

def get_upload_filepath_from_filename(filename):
    return os.path.join(app.config['UPLOAD_FOLDER'], filename)

def get_matrix_from_form_data(form_data, num_rows):
    matrix = []

    row_counter = -1
    form_items_counter = 0
    for key in request.form:
        value = request.form.get(key)

        if form_items_counter % num_rows == 0:
            matrix.append([])
            row_counter += 1

        matrix[row_counter].append(value)
        form_items_counter += 1

    return matrix


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
