from flask import request, redirect, flash, url_for, render_template, make_response
from flask_restful import Resource
import sys
import traceback
import json
import os
import jinja2

# jinja_env=jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), '..', 'site','templates'))) 
# print(os.path.join(os.path.dirname(__file__), '..','site', 'templates'))

ALLOWED_EXTENSIONS = set(['csv', 'txt', 'pdf'])

'''
    Parse text document.
'''
def parse_txt_data(data):
    data = data.decode('utf-8').split("\r\n\r\n")
    return [' '.join(line.split('\r\n')).replace('\\u', ' ') for i, line in enumerate(data)]

def allowed_file(filename):
    return '.' in filename and filename.split('.')[-1].lower() in ALLOWED_EXTENSIONS

class ReadFile(Resource):
    '''
        Controller for api/read_file
    '''
    MISSING_FILE = "POST api/read_file has no file attached."
    INCORRECT_FILE_TYPE = "POST api/read_file the attached file type is incorrect."

    def __init__(self):
        pass

    def get(self):
        print("I am in GET.")
        return redirect(url_for('site.homepage'))
        # if request.args is None:
        #     raise ValueError(self.EMPTY_ARGS)
        
    def post(self):
        '''
            Returns similar paragraphs.
            :return: 
            list of similar paragraphs. (correct THIS)
        '''

        if 'file' not in request.files:
            flash('No file uploaded.')
            return redirect(url_for('site.homepage'))

        rfile = request.files['file']

        if rfile.filename == '':
            print("api/read_file. Check file is missing.")
            return redirect(url_for('site.homepage'))

        if not allowed_file(rfile.filename):
            print("api/read_file. Check incorrect file extension.")
            return redirect(url_for('site.homepage'))
        
        if rfile.filename.split('.')[-1].lower() == 'txt':
            data = rfile.read()
            data = parse_txt_data(data)
            title = rfile.filename
            headers = {'Content-Type': 'text/html'}
            return make_response(render_template('base.html', my_data=data, title=title),200,headers)
        else:
            response = {'response': 'success'}

        # try:
        #     csv_data = rfile.read()
        #     print(csv_data)
        #     print(tfidf_similartext(csv_data))
        #     return "File read"
        #     # return self.tfidf_similartext(csv_data)
        # except:
        #     traceback.print_exception(*sys.exc_info())
        #     response = {'response': 'success'}
        return response

