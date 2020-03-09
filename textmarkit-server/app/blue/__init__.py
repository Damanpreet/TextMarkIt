from flask import Flask

app = Flask(__name__, instance_relative_config=True)#, template_folder='/site/templates')

from celery import Celery
from app.config import cfg
from app.blue.utils import mongo_connect

celery = Celery(app.name, broker=cfg.CELERY_BROKER_URL)
celery.conf.update(app.config)

usr = cfg.MONGO_DB_USER
pwd = cfg.MONGO_DB_PASS

db = mongo_connect()
collection_name = 'SampleCollection'
collection=db[collection_name]

def _initialize_blueprints(app):
    from app.blue.site.routes import mod
    from app.blue.api.routes import api_bp

    app.register_blueprint(mod)
    app.register_blueprint(api_bp, url_prefix='/api')

def _initialize_errorhandlers(app):
    from app.blue.errors import errors
    app.register_blueprint(errors)

_initialize_errorhandlers(app)
_initialize_blueprints(app)
