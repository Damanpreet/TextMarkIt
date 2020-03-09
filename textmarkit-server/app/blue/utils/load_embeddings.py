'''
    Version - 1.0
    Date - 03/02/2020
    
    Script function -
    This script consists of functions to load word embeddings from the database.
'''
from app.blue import collection
import numpy as np

def query_embeddings(per_page, offset):
    try:
        query = [
            {
                "$match":
                    {
                        "type": "embeddings"
                    }
            },
            {
                "$project" : {
                        "_id" : 0,
                        "embedding" : 1
                }
            },
            {
                "$skip" : offset
            },
            {
                "$limit" : per_page
            },
            {
                "$sort": {
                    "_id": 1
                }
            }]

        result = collection.aggregate(query)
        results = []
        for data in result:
            results.append(data['embedding'])
        return np.array(results)
    except:
        print("Error connecting to database")

def query_para_embeddings(para_id):
    '''
        Function to query embeddings for specified paragraphs
    '''
    try:
        query = [
            {
                "$match":
                    {
                        "type": "embeddings",
                        "para_id": {
                            "$in": para_id
                        }
                    }
            },
            {
                "$project" : {
                        "_id" : 0,
                        "embedding" : 1
                }
            },
            {
                "$sort": {
                    "_id": 1
                }
            }]

        result = collection.aggregate(query)
        results = []
        for data in result:
            results.append(data['embedding'])
        return np.array(results)
    except:
        print("Error connecting to database")
