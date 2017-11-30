from flask import Flask
from flask import render_template, send_file
import os


app = Flask(__name__)


###################################################
# home page
###################################################
@app.route('/')
def index():
    return render_template('index.html')


###################################################
# test page
###################################################
@app.route('/test_image')
def test_image():
    img_path = '/home/pi/HW8_PhotoBooth/camera/screenshot/'
    return render_template('test_image.html', tree=make_tree(img_path))


@app.route('/return_file/<filename>')
def return_file(filename):
    return send_file('/home/pi/HW8_PhotoBooth/flask/static/camera_image/' + filename, attachment_filename=filename)


###################################################
# real page
###################################################
@app.route('/camera_image')
def camera_image():
    camera_path = '/home/pi/HW8_PhotoBooth/ImageStorage/'
    return render_template('camera_image.html', tree=make_tree(camera_path))


@app.route('/camera_image/<filename>')
def screenshots(filename):
    return send_file('/home/pi/HW8_PhotoBooth/ImageStorage/' + filename, 
            attachment_filename=filename)


# rendering file tree 
def make_tree(path):
    tree = dict(name=os.path.basename(path), children=[])
    try: lst = os.listdir(path)
    except OSError:
        pass #ignore errors
    else:
        lst.sort()
        for name in lst:
            fn = os.path.join(path, name)
            if os.path.isdir(fn):
                tree['children'].append(make_tree(fn))
            else:
                tree['children'].append(dict(name=name))
    return tree


# tests
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
