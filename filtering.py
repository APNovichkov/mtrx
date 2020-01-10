from random import randint
import matplotlib.image as img
import numpy as np

# Some default kernels

f_outline = [
    [-1, -1, -1],
    [-1, 8, -1],
    [-1, -1, -1]
]

f_sharp = [
    [0, -1, 0],
    [-1, 5, -1],
    [0, -1, 0]
]

list_of_filters = [f_sharp, f_outline]

# Main Functions

def get_random_filter():
    """Return random filter from premade filters."""

    random_int = randint(0, len(list_of_filters) - 1)
    return list_of_filters[random_int]

def apply_filter(original_image_filepath, filter, output_path):
    """Apply a kernel filter to input image and return filename of new image."""

    original_image = img.imread(original_image_filepath)

    # Get dimensions of the input image
    ROWS = original_image.shape[0]
    COLS = original_image.shape[1]

    d = np.zeros((ROWS, COLS, 3), dtype=int).tolist()
    for k in range(3):
        for i in range(ROWS - 2):
            for j in range(COLS - 2):
                s = 0
                for ii in range(3):
                    for jj in range(3):
                        s += original_image[i + ii][j + jj][k] * filter[ii][jj]
                d[i + 1][j + 1][k] = int(s)
    d = np.array(d)

    edited_image = np.clip(d, 0, 255)
    edited_image = edited_image.astype('uint8')

    edited_image_filename = os.path.basename(original_image_filepath).split('.')[0] + "_edited.jpg"

    edited_image_filepath = os.path.join(output_path, edited_image_filename)
    img.imsave(edited_image_filepath, edited_image)

    return edited_image_filename


# Helper Functions


if __name__ == "__main__":
    print("Here is your random filter: {}".format(get_random_filter()))
