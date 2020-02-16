'''
    source: https://harishvc.com/2015/04/15/pagination-flask-mongodb/
    Paginate data
'''
from flask import request, make_response, render_template, url_for, Response
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
        #                 'type': 0,
        #                 'para_id': 0,
        #             }
        #         },
        #         {
        #             "$skip": offset
        #         },
        #         {
        #             "$limit": per_page
        #         }
        #     ]

        # pipeline = [
        #     {'$match': {'type': 'text'}},
        #     {'$group': {'_id': 0, 'total': {'$sum': 1}, 'text': {'$push': '$$CURRENT'}}},
        #     {'$project': {'_id': 0, 'text': 1, 'total': 1}},
        #     {'$unwind': '$text'},
        #     {"$skip" : 2},
        #     {'$limit': 2}
        # ]

        query = [
            {
                "$match":
                    {
                        "type": "text"
                    }
            },
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
            print("page no is not present in the get request.") 
            pageno=1
        
        try:
            identifier = request.form['identifier']
        except:
            identifier = "first"
            print("no identifier found.")
        
        print("Fetching page: ", pageno)
        per_page = cfg.PER_PAGE
        
        offset = (pageno-1)*per_page
        currresult = query_data(per_page, offset)
        
        offset = pageno*per_page
        nextresult = query_data(per_page, offset)

        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('paginate.html', my_data=currresult, prevresult={'total':0}, nextresult=nextresult, pageno=pageno, identifier=identifier), 200, headers)        
        # destination = url_for('api.paginate')
        # return Response(response=json.dumps({'url': destination, "my_data":currresult, "prevresult":{'total':0}, "nextresult":nextresult, "pageno":pageno, "identifier": identifier}), status=200, mimetype='text/json')

    def post(self):
        '''
            Post requests for api/paginate.
        '''
        print("I am in POST.")
        try:
            pageno = int(request.form['pageno'])
        except:
            print("no page is not present in the post request.") 
            pageno=1
        
        # calculate weights in background. check later.
        per_page = cfg.PER_PAGE
        print("Fetching page: ", pageno)

        try:
            prevresult = eval(request.form['prevresult'])
            print("Previous results found.")
        except:
            if pageno!=1:
                offset = (pageno-2)*per_page
                prevresult = query_data(per_page, offset)
            else: prevresult={'total':0}

        try:
            currresult = eval(request.form['currresult'])
            print("Current results found.")
        except:
            offset = (pageno-1)*per_page
            prevresult = query_data(per_page, offset)

        try:            
            nextresult = eval(request.form['nextresult'])
            print("Next results found.")
        except:
            offset = pageno*per_page
            nextresult = query_data(per_page, offset)
        
        try:
            identifier = request.form['identifier']
        except:
            identifier = "next"
            print("no identifier found. default is next.")

        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('paginate.html', my_data=currresult, prevresult=prevresult, nextresult=nextresult, pageno=pageno, identifier=identifier), 200, headers)        
        
        # destination = url_for('api.paginate')
        # return Response(response=json.dumps({'url': destination, "my_data":currresult, "prevresult":prevresult, "nextresult":nextresult, "pageno":pageno, "identifier": identifier}), status=200, mimetype='text/json')

