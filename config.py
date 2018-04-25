import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'override this please!'
    DEBUG = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    NEWSAPI_KEY = os.environ.get('NEWSAPI_KEY')


class DevelopementConfig(Config):
    DEBUG = True
    TEMPLATE_AUTO_RELOAD = True
    EXPLAIN_TEMPLATE_LOADING = True
    GOOGLEMAPS_KEY = 'AIzaSyDeKO22YmX_a5lsoeImXUkWx7d0H36k3sY'
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir,
                                                          'dev-db.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
                              'sqlite://'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir,
                                                          'data.sqlite')


config = {
    'development': DevelopementConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopementConfig
}
