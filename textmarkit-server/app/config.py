from easydict import EasyDict as cfg

# configuration for Celery.
cfg.CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379'
cfg.CELERY_BROKER_URL = 'redis://127.0.0.1:6379'
cfg.SESSION_TYPE = 'filesystem'
cfg.SECRET_KEY = 'super secret key'

# configuration for MongoDB
cfg.MONGO_URI = 'mongodb://dpreet:damanpreet@capstone:31740/flaskfile'
cfg.MONGO_DB_USER = 'dpreet'
cfg.MONGO_DB_PASS = 'damanpreet'

# configuration for pagination
cfg.PER_PAGE = 100

# configuration for similarity threshold
cfg.TOP_SIMILAR = 6
cfg.TOP_THRESHOLD = 0.01
cfg.SIMILARITY_UPDATE_THRESH = 0.02
