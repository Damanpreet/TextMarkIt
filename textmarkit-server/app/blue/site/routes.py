from flask import Blueprint
# from app import app
from flask import render_template

mod = Blueprint('site', __name__, template_folder='templates')

@mod.route('/')
def homepage():
    # list_example = ['Alvin', 'Simon', 'Theodore']
    # return render_template('base1.html', list_example=list_example)
    return render_template('index.html')

@mod.route('/contact/')
def contact(name=None):
    return render_template('contact.html')

@mod.route('/404/')
def pagenotfound(name=None):
    return render_template('404.html')
