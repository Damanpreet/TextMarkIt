from flask import Blueprint
from flask_restful import Api

from app.blue.api.similar_text_tfidf import SimilarTextTFIDF
from app.blue.api.read_file import ReadFile

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

api.add_resource(SimilarTextTFIDF, '/similar_text_tfidf')
api.add_resource(ReadFile, '/read_file')