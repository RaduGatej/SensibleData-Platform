import os

#Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#Root directory of the project
ROOT_DIR = '/home/user/sensible_data_platform/'

#Root url prefix
ROOT_URL = '/sensible-data/'

#Base url prefix (the entire thing)
BASE_URL = 'https://nowhere.com/sensible-data/'

#URLS TO FIRST /
TRUST_ROOTS = ["https://nowhere.com/"]

#Secret key for the project
#Can be generated with

#import uuid, hashlib
#str(hashlib.sha256(str(uuid.uuid4())).hexdigest())
SECRET_KEY = '1234'


#Databses
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': ROOT_DIR+'SECURE_data.db',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

SERVICE_NAME = "Sensible Data"
SUPPORT_MAIL = "support@sensible.dtu.dk"
