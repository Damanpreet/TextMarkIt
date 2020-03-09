from pymongo import MongoClient

def mongo_connect():
	try:
		conn = MongoClient('127.0.0.1', 27017)
		print("Connected to database successfully!")
		database_name = 'SampleDatabase'

		db=conn[database_name]
		return db
	except:
		print("Could not connect to database.")
		return 
