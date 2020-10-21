import os
from collections import namedtuple

from flask import Flask, render_template, redirect, url_for, request


app = Flask(__name__)

Doc=namedtuple('Doc','text')
docs=[]
docs.clear()

@app.route('/', methods=['GET', 'POST'])
def main_page():
    # return render_template('common_docs.html')
    return render_template('common_docs.html', docs=docs)


APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/upload", methods=['POST'])
def upload():
    target = os.path.join(APP_ROOT, "files\\")
    print(target)

    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist("file"):
        print(file)
        filename = file.filename
        destination = "\\".join([target, filename])
        print(destination)
        file.save(destination)

    # print("File upload")
    return render_template('complete.html')


@app.route('/add_text', methods=['POST'])
def add_text():
    text=request.form['text']
    docs.clear()
    docs.append(Doc(text))
    return redirect(url_for('main_page'))

if __name__ == '__main__':
    app.run()