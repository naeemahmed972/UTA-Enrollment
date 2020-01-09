import os

class Config(object):
    
    SECRET_KEY = os.environ.get('SECRET_KEY') or b'G\xcc*\xf9\xf7u\x87\xc0\x99\x98\xb3\xf0\x992\xbc\xe3'

    MONGODB_SETTINGS = { 

        'db': 'UTA_Enrollment',
        # 'host': 'mongodb://localhost:27017/UTA_Enrollment'
    }