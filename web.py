import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

from flask import send_from_directory
import requests

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(app.root_path, 'melody_separator/src/input')
# os.makedirs(uploads_dir)
ALLOWED_EXTENSIONS = {'wav'}

# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print("filename: ", filename)
            file.save(os.path.join(UPLOAD_FOLDER, secure_filename(filename)))
            #passing parameter
            paras = {"input":filename}
            response = requests.get(url="http://127.0.0.1:5002/", params = paras)
            return redirect(url_for('download_file', name=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(UPLOAD_FOLDER, name)


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080,debug=True)