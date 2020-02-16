from flask import request, redirect, flash, url_for
from flask_restful import Resource
import sys
import traceback
import json
import os
import jinja2
from app.blue.utils.parse_html import parse_html
from app.blue.tasks import compute_tfidf
from app.blue.utils.tfidfsimilarity import tfidf_similartext
import pymongo
from pymongo import MongoClient
from app.blue import collection
import pandas as pd
from app.config import cfg
import codecs

ALLOWED_EXTENSIONS = set(['csv', 'txt', 'html'])

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
            Tasks:
        
            1. Read and parse the uploaded file. 
            2. Store the data in the Database.
            3. Compute embeddings in the background.
        '''

        try:
            if 'file' not in request.files:
                flash('No file uploaded.')
                return redirect(url_for('site.homepage'))

            rfile = request.files['file']
            fname = rfile.filename

            if fname == '':
                print("api/read_file. Check file is missing.")
                return redirect(url_for('site.homepage'))

            if not allowed_file(fname):
                print("api/read_file. Check incorrect file extension.")
                return redirect(url_for('site.homepage'))
            
            print("File type: ", rfile.content_type)

            if rfile.content_type == 'text/plain':
                data = rfile.read()
                data = parse_txt_data(data)

                # for the first 100 paragraphs that renders on the first page.
                print("length of data: ", len(data))
                compute_tfidf.apply_async(queue='high_priority', priority=0, args=[data[:cfg.PER_PAGE], 'txt', 100])

                df=pd.DataFrame(data, columns=['text'])
                records = list(df.T.to_dict().values())
                count = 0
                for item in records:
                    item.update({'para_id': count, 'type': "text"})
                    count+=1
                
                try:
                    collection.remove({}) # remove anything that is present in the collection.
                    collection.insert(records)
                    print("inserted records into the database.")
                except Exception as e:
                    print(e)
                    print("Failed to insert record.")
                    return redirect(url_for('site.pagenotfound'))

                # for the complete data.
                compute_tfidf.apply_async(queue='default', args=[data, 'txt'])             
                return redirect(url_for('api.paginate'), code=303)
            
            elif rfile.content_type == "text/html":
                data = rfile.read()
                # if os.name == 'nt': 
                data = data.decode('cp1252')
                data = parse_html(data)

                try:
                    collection.remove({}) # remove anything that is present in the collection.
                except:
                    print("error while removing from the collection.")
                    return 

                # find the tf idf vectors for the first page.
                compute_tfidf.apply_async(queue='high_priority', priority=0, args=[data[:cfg.PER_PAGE], 'txt', 100])

                df=pd.DataFrame(data, columns=['text'])
                records = list(df.T.to_dict().values())
                count = 1
                for item in records:
                    item.update({'para_id': count, 'type': "text"})
                    count+=1

                try:
                    collection.insert(records)
                    print("inserted records into the database.")
                except Exception as e:
                    print(e)
                    print("Failed to insert record.")
                    return redirect(url_for('site.pagenotfound'))
                
                # find the tf idf vectors for the complete data.
                compute_tfidf.apply_async(queue='high_priority', priority=0, args=[data, 'txt', 100])

                return redirect(url_for('api.paginate'), code=303)
            else:
                response = {'response': 'success'}

            return response
        except Exception as e:
            print("oh crap! error!")
            print("Error: ", e)
            return redirect(url_for('site.pagenotfound'))