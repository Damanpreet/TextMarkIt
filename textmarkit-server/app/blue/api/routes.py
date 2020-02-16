from flask import Blueprint
from flask_restful import Api

# from app.blue.api.similar_text_tfidf import SimilarTextTFIDF
from app.blue.api.read_file import ReadFile
from app.blue.api.paginate import Paginate
from app.blue.api.similarity import Similarity, DeleteSimilarity
from app.blue.api.load_suggestions import LoadSuggestions

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# api.add_resource(SimilarTextTFIDF, '/similar_text_tfidf')
api.add_resource(ReadFile, '/read_file')
api.add_resource(Paginate, '/paginate')
api.add_resource(Similarity, '/similarity')
api.add_resource(DeleteSimilarity, '/delete_similarity')
api.add_resource(LoadSuggestions, '/load_suggestions')
