from app.blue import celery
from app.blue.utils.tfidfsimilarity import tfidf_similartext

@celery.task
def compute_tfidf(data, file_format):
	return tfidf_similartext(data, file_format)


