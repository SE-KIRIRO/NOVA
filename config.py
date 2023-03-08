import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    NOVA_MAIL_SUBJECT_PREFIX = '[NOVA]'
    NOVA_MAIL_SENDER = os.environ.get("MAIL_USERNAME")
    NOVA_ADMIN = os.environ.get('NOVA_ADMIN')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    NOVA_POSTS_PER_PAGE = int(os.environ.get("NOVA_POSTS_PER_PAGE"))

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

config = {
    "development": DevelopmentConfig,
    "testing" : TestingConfig,
    "production" : ProductionConfig,
    "default": DevelopmentConfig
}