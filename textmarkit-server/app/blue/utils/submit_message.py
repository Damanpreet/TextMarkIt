'''
    Version - 1.0
    Date - 15/02/2020
    
    Script function -
    This script consists of function to submit messages in the database.
'''
from app.blue import db
import numpy as np

def submit_msg(name, email, phone, message):
    try:
        collection_name = 'UserCollection'
        db[collection_name].insert_one({'name': name, 'email': email, 'phone': phone, 'message': message})
        return True
    except:
        print("Error connecting to database")
        return False