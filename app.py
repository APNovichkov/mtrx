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

# host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/mtrxio')
# client = MongoClient(host=f'{host}?retryWrites=false')
# db = client.get_default_database()
# uploads = db['uploads']

app.current_filter = []

# Route Functions

@app.route("/")
def welcome():
    """Show the welcome page where use can upload an image."""

    return render_template('index.html')

@app.route("/dashboard/<original_filename>/<edited_filename>")
def show_dashboard(original_filename, edited_filename):
    """Shows the dashboard from which all further actions are taken."""

    # Get filepaths of images to show on the show_dashboard
    # These are not full paths
    original_filepath = os.path.join(UPLOAD_FOLDER, original_filename)

    print("Original filepath: {}".format(original_filepath))

    edited_filepath = os.path.join(UPLOAD_FOLDER, edited_filename)

    print("Current filter is: {}".format(app.current_filter))

    if edited_filename == "None":
        edited_filepath = "None"

    return render_template("dashboard.html", input_filter=app.current_filter, original_filename=original_filename, original_filepath=original_filepath, edited_filepath=edited_filepath)

@app.route("/generate-image/<original_filename>", methods=['POST'])
def generate_image(original_filename):
    print("Need to apply filter and generate new image from this file: {}".format(original_filename))

    # Define size of convolution matrix
    rows = 3

    # Get filter from input user data
    filter = get_matrix_from_form_data(request.form, rows)
    app.current_filter = filter
    print("This is the user inputted filter: {}".format(filter))

    # Get filepath for original image
    filepath = get_upload_filepath_from_filename(original_filename)

    # Send that filepath over for processing to filtering module
    edited_filename = filtering.apply_filter(filepath, filter, app.config['UPLOAD_FOLDER'])

    return redirect(url_for('show_dashboard', original_filename=original_filename, edited_filename=edited_filename))


@app.route("/upload", methods=['POST'])
def upload_image():
    """Upload and compresses image to local directory for future processing."""

    # Check if file is in request object
    if 'file' not in request.files:
        print("File not in request")
        return redirect(url_for('index'))

    # If it is in request, get the file
    file = request.files['file']

    # Check to make sure that there is an actual file in there
    if file.filename == "":
        print("User did not select file")
        return redirect(url_for('index'))

    # Check if file is allowed and save it in the directory
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # inserted_id = uploads.insert_one(filename).inserted_id

        # print("Inserted Id: {}".format(inserted_id))

        # Compress the file
        filename = compress_file(filename)

        # Set filter to random filter

        print("filtering filter: {}".format(filtering.get_random_filter))

        app.current_filter = filtering.get_random_filter()

        print("app.current_filter: {}".format(filtering.get_random_filter()))

        # Show the dashboard
        return redirect(url_for('show_dashboard', original_filename=filename, edited_filename="None"))

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

# Helper Functions

def get_upload_filepath_from_filename(filename):
    """Return full path to the uploaded file."""

    return os.path.join(app.config['UPLOAD_FOLDER'], filename)

def get_matrix_from_form_data(form_data, num_rows):
    """Get the filter matrix from input form data."""

    matrix = []

    row_counter = -1
    form_items_counter = 0
    for key in request.form:
        value = request.form.get(key)

        if form_items_counter % num_rows == 0:
            matrix.append([])
            row_counter += 1

        matrix[row_counter].append(int(value))
        form_items_counter += 1

    return matrix


def compress_file(filename):
    """Compress input file and replace it with compressed version in jpg format."""

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    # Open input file
    foo = Image.open(filepath)
    foo = foo.resize((int(foo.size[0] / 10), int(foo.size[1] / 10)), Image.ANTIALIAS)

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
    """Return true if inputted file is of valid format."""

    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.run(debug=True)
