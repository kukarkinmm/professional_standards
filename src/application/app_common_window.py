import os
from collections import namedtuple

from flask import Flask, render_template, redirect, url_for, request, jsonify, flash, send_from_directory

from werkzeug.utils import secure_filename

from werkzeug.middleware.shared_data import SharedDataMiddleware


app = Flask(__name__)

Doc=namedtuple('Doc','text')
docs=[]
docs.clear()

@app.route('/', methods=['GET', 'POST'])
def main_page():
    # return render_template('common_docs.html')
    return render_template('common_docs.html', docs=docs)


APP_ROOT = os.path.dirname(os.path.abspath(__file__))
# ALLOWED_EXTENSIONS = set(['pdf', 'docx', 'doc', 'txt'])
ALLOWED_EXTENSIONS = set(['pdf'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/upload", methods=['POST'])
def upload():
    UPLOAD_FOLDER = os.path.join(APP_ROOT, "files\\")
    # print(UPLOAD_FOLDER)

    if not os.path.isdir(UPLOAD_FOLDER):
        os.mkdir(UPLOAD_FOLDER)

    for file in request.files.getlist("file"):
        print(file)
        if file and allowed_file(file.filename):
            # filename = file.filename
            filename = secure_filename(file.filename)
            destination = "\\".join([UPLOAD_FOLDER, filename])
            print(destination)
            file.save(destination)
            return render_template("complete.html")

    # print("File uploaded")
    return render_template("uploading_error.html")


@app.route('/add_text', methods=['POST'])
def add_text():
    text=request.form['text']
    docs.clear()
    docs.append(Doc(text))
    return redirect(url_for('main_page'))

#####
files=[
    {'id':1,
     'file':'C:/Users/nelly/PycharmProjects/professional_standards/src/application/files/1_st_annc_slotine.pdf'
    },
    {'id':2,
     'file':'bla-bla-bla'
    }
]

@app.route('/rpds/api/v1.0/files', methods=['GET'])
def get_files():
    return jsonify({'files': files})
####


if __name__ == '__main__':
    app.run()