from collections import namedtuple

from flask import Flask, render_template, redirect, url_for, request


app = Flask(__name__)

Doc=namedtuple('Doc','text')
docs=[]
docs.clear()


@app.route('/', methods=['GET', 'POST'])
def main_page():
 return render_template('common_docs.html', docs=docs)


@app.route('/add_text', methods=['POST'])
def add_text():
    text=request.form['text']
    docs.clear()
    docs.append(Doc(text))
    return redirect(url_for('main_page'))



if __name__ == '__main__':
    app.run()