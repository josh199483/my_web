import os
basedir = os.path.abspath(os.path.dirname(__file__))

from instance.secret import POSTGRESQL_USER, POSTGRESQL_PASSWORD, POSTGRESQL_HOST, POSTGRESQL_PORT, POSTGRESQL_DATABASE



class Config:
    ##### Flask.config - http://flask.pocoo.org/docs/0.12/config/
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'this-really-needs-to-be-changed'  # 保護 session遭到篡改的機制
    
    ##### WTForm - http://flask-wtf.readthedocs.io/en/stable/form.html
    WTF_CSRF_ENABLED = False    # 設為False則所有post請求都不會受到csrf的保護，在成功測試rest API之後要改為True以做測試
    
    ##### PyMongo
    # MONGO_HOST = '192.168.124.81'
    # MONGO_DBNAME = 'pome'
    # MONGO_PORT = 27017
    # MONGO_MAX_POOL_SIZE = 20
    # MONGO_CONNECT = False
    # MONGO_URI = 'mongodb://root:pome@192.168.124.81:27017/pome'

    ##### SQLAlchemy - http://flask-sqlalchemy.pocoo.org/2.3/config/
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 不設會一直跑 WARNING
    SQLALCHEMY_DATABASE_URI = 'postgres://{0}:{1}@{2}:{3}/{4}'.format(POSTGRESQL_USER,POSTGRESQL_PASSWORD,POSTGRESQL_HOST,POSTGRESQL_PORT,POSTGRESQL_DATABASE)
    SQLALCHEMY_ECHO = False  # [False, True] - True時, SQLAlchemy錯誤資訊會由 stderr輸出

    ##### DebugToolbarExtension - https://pypi.python.org/pypi/Flask-DebugToolbar
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar
    DEBUG_TB_INTERCEPT_REDIRECTS = False    # 若依照預設為 True時, 所有 redirect都會失效

    ##### Server
    USE_RELOADER = True # should the server automatically restart the python process if modules were changed?
    THREADED = True # should the process handle each request in a separate thread?

    # Cache 
    CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.

    # flask_upload settings
    UPLOADED_IMG_DEST = r'D:\test_upload_images'
    UPLOADED_IMG_URL = '\\test_upload_images\\'


    @staticmethod
    def init_app(app):
        pass



class ProductionConfig(Config):
    DEBUG_TB_ENABLED = False
    # MONGO_HOST = '127.0.0.1'



class DevelopmentConfig(Config):
    DEBUG = True
    DEBUG_TB_ENABLED = True
    # MONGO_URI = 'mongodb://192.168.124.81:27017/pome'
    
    ##### Redis Cache
    # CACHE_TYPE = 'redis' # pip install redis
    # CACHE_REDIS_URL = 'redis://192.168.124.81:6379/2'

    ##### Redis
    # REDIS_HOST = 'localhost'
    # REDIS_PORT = 6379
    # REDIS_DB = 0
    # REDIS2_URL = 'redis://192.168.124.81:6379/2'
    ### 回傳 keys 元素的時候不會是 bytes
    # REDIS2_CHARSET = 'utf-8'
    # REDIS2_DECODE_RESPONSES = True


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    # MONGO_DBNAME = 'test'
    # MONGO_HOST = '127.0.0.1'


cfg = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
