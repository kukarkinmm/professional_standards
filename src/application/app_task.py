from collections import namedtuple

from flask import Flask, render_template, redirect, url_for, request


app = Flask(__name__)

Doc=namedtuple('Doc','text')
docs=[]
docs.clear()


@app.route('/', methods=['GET', 'POST'])
def main_page():
    return render_template('main.html', docs=docs)


@app.route('/add_text', methods=['POST'])
def add_text():
    text=request.form['text']

    docs.clear()
    docs.append(Doc(text))

    file_int=request.form['AttachedFile']
    with open(file_int) as file:
        text_1 = file.read()

        

    return redirect(url_for('main_page'))

