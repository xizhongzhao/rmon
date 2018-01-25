""" rmon.config  the config of rmon file """
import os

class DevConfig:
    """ the config of dev """
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    TEMPLATES_AUTO_RELOAD = True

class ProductConfig(DevConfig):
    """ the config of production """
    DEBUG = False
# the path of sqlite
    path = os.path.join(os.getcwd(),'rmon.db').replace('\\','/')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' %path
