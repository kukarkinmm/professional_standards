import os
from collections import namedtuple

from flask import Flask, render_template, redirect, url_for, request, jsonify, flash, send_from_directory, abort
from werkzeug.utils import secure_filename

from src.models.model import Model
from src.parsers.pdf_parser import PdfParser

app = Flask(__name__)
Doc = namedtuple('Doc', 'text')
docs = []
model = Model()


@app.route('/', methods=['GET', 'POST'])
def main_page():
    #    # return render_template('common_docs.html')
    ##    def upload_file():
    #        if request.method == 'POST':
    #            # check if the post request has the file part
    #            if 'file' not in request.files:
    #                flash('No file part')
    #                return redirect(request.url)
    #            file = request.files['file']
    #            # if user does not select file, browser also
    #            # submit an empty part without filename
    #            if file.filename == '':
    #                flash('No selected file')
    #                return redirect(request.url)
    #            if file and allowed_file(file.filename):
    #                filename = secure_filename(file.filename)
    #                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    #              return redirect(url_for('uploaded_file',
    #                                       filename=filename))
    return render_template('common_docs.html', docs=docs)


APP_ROOT = os.path.dirname(os.path.abspath(__file__))
# ALLOWED_EXTENSIONS = set(['pdf', 'docx', 'doc', 'txt'])
ALLOWED_EXTENSIONS = set(['pdf'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route("/upload", methods=['POST'])
def upload():
    text = request.form['text']
    if bool(text) is False:
        UPLOAD_FOLDER = os.path.join(APP_ROOT, "files")

        if not os.path.isdir(UPLOAD_FOLDER):
            os.mkdir(UPLOAD_FOLDER)

        for file in request.files.getlist("file"):
            if file and allowed_file(file.filename):
                # filename = file.filename
                filename = secure_filename(file.filename)
                destination = os.path.join(UPLOAD_FOLDER, filename)
                # destination = "".join([UPLOAD_FOLDER, filename])
                file.save(destination)
                parser = PdfParser()
                text = parser.extract_relevant(destination)
                result = model.closest_standards(text)
                output = "".join([f"{r[1]}\t-\t{r[0]}\n" for r in result])
                docs.clear()
                docs.append(Doc(output))
                return redirect(url_for('main_page'))
    else:
        result = model.closest_standards(text)
        output = "".join([f"{r[1]}\t-\t{r[0]}\n" for r in result])

        docs.clear()
        docs.append(Doc(output))
        return redirect(url_for('main_page'))


@app.route('/add_text', methods=['POST'])
def add_text():
    text = request.form['text']

    result = model.closest_standards(text)
    output = "".join([f"{r[1]}\t-\t{r[0]}\n" for r in result])

    docs.clear()
    docs.append(Doc(output))
    return redirect(url_for('main_page'))


#####
# files=[
#    {'id':1,
#     'file':''
#    },
#    {'id':2,
#     'file':''
#    }
# ]


@app.route('/rpds/api/v1.0/files', methods=['GET'])
def get_files():
    return jsonify({'text': docs[0]})


@app.route('/rpds/api/v1.0/files', methods=['POST'])
def create_text():
    if not request.json:
        abort(400)
    text = {
        'id': docs[-1]['id'] + 1,
        'text': request.json.get('text', ""),
    }
    docs.append(text)
    return jsonify({'text': text}), 201


if __name__ == '__main__':
    app.run(debug=True)
