from app import app
from flask import render_template

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/contact/')
def contact(name=None):
    return render_template('contact.html')