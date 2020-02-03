from flask import Flask
app = Flask(__name__, instance_relative_config=True)#, template_folder='/site/templates')
from celery import Celery
from app.config import cfg
from pymongo import MongoClient

celery = Celery(app.name, broker=cfg.CELERY_BROKER_URL)
celery.conf.update(app.config)

usr = cfg.MONGO_DB_USER
pwd = cfg.MONGO_DB_PASS
try:
    conn = MongoClient('localhost', 27017)
    print("Connected to database successfully!")
except:
    print("Could not connect to database.")

database_name = 'SampleDatabase'
collection_name = 'SampleCollection'

db=conn[database_name]
collection=db[collection_name]

from app.blue.site.routes import mod
from app.blue.api.routes import api_bp

app.register_blueprint(mod)
app.register_blueprint(api_bp, url_prefix='/api')