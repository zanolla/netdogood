# -*- coding: utf-8 -*-

import os

class Config:

    APP_NAME = 'rededobem'
    ADMIN_NAME = 'admin'
    MYENV = 'BaseConfig'
    SECRET_KEY = 'WGsdafHSDFHseFHEweET345@#$%@#55GGS'

    try:
        AWS_KEY = os.environ['AWS_KEY']
        AWS_SEC = os.environ['AWS_SEC']
    except:
        AWS_KEY = 'No AWS Key. Please set AWS_KEY env variable'
        AWS_SEC = 'No AWS Sec. Please set AWS_SEC env variable'


class DevConfig(Config):

    DEBUG = True
    MYENV = 'DevConfig'

    LOGIN_ENFORCE = True
    
    DATABASE_HOST = 'localhost'
    DATABASE_PORT = '27017'
    DATABASE_NAME = 'rededobem'

class TestConfig(Config):

    DEBUG = False
    MYENV = 'TestConfig'

    LOGIN_ENFORCE = False
    
    DATABASE_HOST = 'localhost'
    DATABASE_PORT = '27017'
    DATABASE_NAME = 'rededobem'
  
class ProdConfig(Config):

    DEBUG = False
    MYENV = 'ProdConfig'

    LOGIN_ENFORCE = True

    DATABASE_HOST = '10.103.208.3'
    DATABASE_PORT = '27017'
    DATABASE_NAME = 'rededobem'
 
class CIConfig:

    DEBUG = False
    MYENV = 'CIConfig'

    LOGIN_ENFORCE = False

    DATABASE_HOST = 'localhost'
    DATABASE_PORT = '27017'
    DATABASE_NAME = 'rededobem'


#loads config based on environment variable
try:
    env = os.environ['APP_ENV']
except:
    env = 'dev'

if env == 'dev':
    appconfig = DevConfig
elif env == 'test':
    appconfig = TestConfig
elif env == 'prod':
    appconfig = ProdConfig
