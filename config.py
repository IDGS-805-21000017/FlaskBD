import os
from sqlalchemy import create_engine
import urllib

class Config(object):
    SECRET_KEY = 'Clave nueva'
    SESSION_COOKIE_SECURE=False

class DevelopmentConfig(Config):
    DEBUG=True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@localhost/bdidgs805?charset=utf8mb4'
    SQLALCHEMY_TRACK_MODIFICATIONS=False