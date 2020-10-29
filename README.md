<div style="padding-top: 40px" align="center">
    <h2>Welcome to MTRX!</h2>
</div>


<p align="center">
    <img src="https://img.shields.io/badge/License-MIT-yellow.svg">
    <a href="http://mtrxio.herokuapp.com/">Official Website</a>
</p>
      
<p align="center">
MTRX is an Image Editing web tool that allows you to upload an image and play around with convolution matrices/kernels to see what effect they have on your Image. You can use these 3x3 matrices to sharpen images, find an image's outlines, blur an image, and so on. Be aware of the fact that if your image is larger than 200kb, the server might give you a timeout.
</p>

<br>

<div align="center">
    <img alt="screenshot" src="docs/images/edit2.png">
</div>

<br>

## Table of Contents
- [Installation](#installation)
  - [Manual](#manual)
  - [License](#license)
  - [Examples](#examples)
  - [Contributors](#contributors)

<a name="installation"></a>

## 🚀 Installation

### Manual

```bash
# Clone repo
git clone https://github.com/APNovichkov/mtrx.git
# CD into repo folder and setup python virtual environment
cd mtrx 
python -m venv
# Install python requirements
pip install -r requiremenets.txt
# Run in Terminal :)
python app.py
#or
flask run
```

## Examples

![Example1](/docs/images/home_page.png)
![Example2](/docs/images/input_matrix.png)
![Example3](/docs/images/edit1.png)


## 📝 License

By contributing, you agree that your contributions will be licensed under its MIT License.

In short, when you submit code changes, your submissions are understood to be under the same [MIT License](http://choosealicense.com/licenses/mit/) that covers the project. Feel free to contact the maintainers if that's a concern.

<a name="contributors"></a>

## Contributors

Contributions are welcome!

<table>
  <tr>
    <td align="center"><a href="https://github.com/APNovichkov"><br /><sub><b>Andrey Novichkov</b></sub></a><br /><a href="https://github.com/APNovichkov/mtrx/commits/master" title="Code">💻</a></td>
  </tr>
</table>







