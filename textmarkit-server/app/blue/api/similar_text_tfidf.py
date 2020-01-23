from flask import request, redirect, flash
from flask_restful import Resource
import sys
import traceback
import json
# from app.blue.utils.helper import load_module
from app.blue.utils.tfidfsimilarity import tfidf_similartext
# from utils.tfidfsimilarity import tfidf_similartext

ALLOWED_EXTENSIONS = set(['csv', 'txt', 'pdf'])

def allowed_file(filename):
    return '.' in filename and filename.split('.')[-1].lower() in ALLOWED_EXTENSIONS

class SimilarTextTFIDF(Resource):
    '''
        Controller for api/similar_text_tfidf
    '''
    MISSING_FILE = "POST api/similar_text_tfidf has no file attached."
    INCORRECT_FILE_TYPE = "POST api/similar_text_tfidf the attached file type is incorrect."

    def __init__(self):
        pass

    def get(self):
        # return "Please attach a file"
        pass
    
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
            return "No file"
            return redirect(request.url)

        rfile = request.files['file']

        if rfile.filename == '':
            raise ValueError(self.MISSING_FILE)
            return redirect(request.url)

        if not allowed_file(rfile.filename):
            flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
            raise ValueError(self.INCORRECT_FILE_TYPE)
            return "Incorrect file name"
            # return redirect(request.url)

        try:
            csv_data = rfile.read()
            print(csv_data)
            print(tfidf_similartext(csv_data))
            return "File read"
            # return self.tfidf_similartext(csv_data)
        except:
            traceback.print_exception(*sys.exc_info())
            response = {'response': 'success'}
        return response

