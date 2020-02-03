'''
    source: https://harishvc.com/2015/04/15/pagination-flask-mongodb/
    Paginate data
'''
# from flask.paginate import Paginate
from flask import request, make_response, render_template
from flask_restful import Resource
from app.config import cfg
from app.blue import collection
import json

def query_data(per_page, offset):
    try:
        # query = [{
        #             '$project': {
        #                 '_id': 0,
        #                 'text': 1,
        #             }
        #         },
        #         {
        #             "$skip": offset
        #         },
        #         {
        #             "$limit": per_page
        #         }
        #     ]

        query = [
            {
                "$project" : {
                        "_id" : 0,
                        "text" : 1,
                        "total" : 1
                }
            },
            {
                "$skip" : offset
            },
            {
                "$limit" : per_page
            },
            {
                "$group" : {
                        "_id" : 0,
                        "total" : {
                                "$sum" : 1
                        },
                        "text" : {
                                "$push" : "$$ROOT"
                        }
                }
            }]

        result = collection.aggregate(query)
        results = {'total': 0}
        for data in result:
            for key in data:
                if key=='total': results[key] = data[key]
                elif key=='text':
                    # res=[]
                    # for d in data[key]:
                    #     res.append({'text': d['text']})
                    # results['text'] = res
                    results['text'] = data['text']
        return results
    except:
        print("Error connecting to database")

class Paginate(Resource):
    '''
        Controller for api/paginate.
    '''
    MISSING_FILE = "POST api/read_file has no file attached."
    INCORRECT_FILE_TYPE = "POST api/read_file the attached file type is incorrect."

    def __init__(self):
        pass

    def get(self):
        '''
            Get request for api/paginate.
        '''
        print("I am in GET.")
        
        try:
            pageno = int(request.args['pageno'])
        except:
            print("no page in get request.") 
            pageno=1
        
        print("Fetching page: ", pageno)
        per_page = cfg.PER_PAGE
        
        offset = (pageno-1)*per_page
        currresult = query_data(per_page, offset)
        
        offset = pageno*per_page
        nextresult = query_data(per_page, offset)

        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('paginate.html', my_data=currresult, prevresult={'total':0}, nextresult=nextresult, pageno=pageno), 200, headers)        


    def post(self):
        '''
            Post requests for api/paginate.
        '''
        print("I am in POST.")
        try:
            pageno = int(request.form['pageno'])
        except:
            print("no page in post request.") 
            pageno=1
        
        # calculate weights in background. check later.
        per_page = cfg.PER_PAGE
        print("Fetching page: ", pageno)

        if 'prevresult' not in request.form and pageno!=1:
            offset = (pageno-2)*per_page
            prevresult = query_data(per_page, offset)
        else:   
            print("Previous results found.")
            prevresult = eval(request.form['prevresult'])
        
        if 'currresult' not in request.form:
            offset = (pageno-1)*per_page
            currresult = query_data(per_page, offset)
        else:   
            print("Current results found.")
            currresult = eval(request.form['currresult']) # convert dictionary string to dictionary

        if 'nextresult' not in request.form:
            offset = pageno*per_page
            nextresult = query_data(per_page, offset)
        else:   
            print("Next results found.")
            nextresult = eval(request.form['nextresult'])

        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('paginate.html', my_data=currresult, prevresult=prevresult, nextresult=nextresult, pageno=pageno), 200, headers)        
        # return make_response(render_template('paginate.html', my_data=currresult, pageno=pageno),200,headers)