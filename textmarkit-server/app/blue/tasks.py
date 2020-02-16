from app.blue import celery
from app.blue.utils.tfidfsimilarity import tfidf_similartext
from app.blue.utils import mongo_connect

@celery.task(name='app.blue.tasks.compute_tfidf', autoretry_for=(Exception,), retry_kwargs={'max_retries': 5, 'countdown': 2})
def compute_tfidf(data, file_format, last=0):
	'''
		Aynchronously compute tf-idf vectors using celery task queue
		and store them into the database.
	'''
	try:
		db = mongo_connect()
		collection_name = 'SampleCollection'
		collection = db[collection_name]
		embeddings = tfidf_similartext(data, file_format)
		
		records = []
		count = 1

		for i in range(embeddings.shape[0]):		
			# convert 1-d numpy array into list. 
			records.append({'para_id': count, 'type': "embeddings", 'embedding': embeddings[i].tolist()})
			count+=1
		
		collection.remove({"type": "embeddings"})
		collection.insert(records)
		print("Embeddings are inserted into the database.")
	except Exception as e:
		print("Error message: ", e)
		print("Error while computing and storing the tf-idf vectors.")
	


