# app.py
from flask import Flask, render_template, request

import data_loader
import clustering

app = Flask(__name__)


@app.route('/')
def index():
    error = None
    preview = None
    try:
        data = data_loader.load_data()
        preview = data.head().to_html(
            classes='table table-sm table-striped mb-0', index=False, na_rep='-')
    except FileNotFoundError as exc:
        error = str(exc)
    return render_template('index.html', preview=preview, error=error)


@app.route('/result', methods=['POST'])
def result():
    return 'TODO: dashboard'  # dilengkapi penuh di Task 6


if __name__ == '__main__':
    app.run(debug=True)
