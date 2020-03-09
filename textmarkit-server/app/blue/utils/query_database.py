'''
    Version - 1.0
    Date - 08/03/2020
    
    Script function -
    This script consists of functions to query the database.
'''
from app.blue import collection
import numpy as np


def query_similarity_info(query):
    '''
        Function to query the similarity information.
        Args:
        :query - query

        Returns cursor to the documents found by matching the query.
    '''
    try:
        return collection.find(query)
    except:
        print("Error while fetching similarity info")


def update_similar(query, value):
    '''
        Function to update a document.

        Args:
        :query: query
        :value: values to be updated
    '''
    try:
        collection.update_one(query, value)
    except Exception as e:
        print("Error: ", e)
        print("Error while updating similarity array to database.")


def insert_database(query):
    '''
        Insert into the database.
        Args:
        :query - query for insertion

        Returns the object id of the inserted document.
    '''
    try:
        return collection.insert(query)
    except Exception as e:
        print("Error while inserting into the database.")
        print("Error: ", e)


def query_similarity_info_one(query):
    '''
        Function to query the similarity information.
        Args:
        :query - Query to find the similar document.

        Returns the object id of the document found by matching the query.
    '''
    try:
        return collection.find_one(query)
    except:
        print("Error while fetching similarity info")

def remove_document(query):
    '''
        Remove a document from the collection.
        Args:
        :query - Query for the document to be removed.
    '''
    try:
        collection.remove(query)
    except Exception as e:
        print("Document removed.")
        print("Error: ", e)
