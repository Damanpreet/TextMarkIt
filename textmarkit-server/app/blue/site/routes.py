from flask import Blueprint, request
# from app import app
from flask import render_template
from app.blue.utils.submit_message import submit_msg

mod = Blueprint('site', __name__, template_folder='templates')

@mod.route('/')
def homepage():
    # list_example = ['Alvin', 'Simon', 'Theodore']
    # return render_template('base1.html', list_example=list_example)
    return render_template('index.html')

@mod.route('/contact/')
def contact(name=None):
    return render_template('contact.html')

@mod.route('/tutorial/')
def tutorial(name=None):
    return render_template('tutorial.html')

@mod.route('/404/')
def pagenotfound(name=None):
    return render_template('404.html')

@mod.route('/submit_message', methods=['POST'])
def submit_message():
    print(request.form)
    try:
        name = request.form['txtName']
    except:
        name = "" 

    try:
        email = request.form['txtEmail']
    except:
        email = "" 

    try:
        phone = request.form['txtPhone']
    except:
        phone = "" 

    try:
        msg = request.form['txtMsg']
    except:
        msg = "" 
       
    if submit_msg(name, email, phone, msg):
        return "success"
    else:
        return "failure"
