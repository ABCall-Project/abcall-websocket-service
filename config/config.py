import os
from dotenv import load_dotenv

environment = os.getenv('FLASK_ENV')

if environment == 'local':
    load_dotenv(dotenv_path='.env.local')
elif environment == 'test':
    load_dotenv(dotenv_path='.env.test')
else:
    load_dotenv(dotenv_path='.env')

class Config:
    ENVIRONMENT = environment
    APP_NAME=os.getenv('APP_NAME')
    URL_REPORTS_SERVICE=os.getenv('URL_REPORTS_SERVICE')