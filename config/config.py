import os
from dotenv import load_dotenv

class Config:
    def __init__(self):
        environment = os.getenv('FLASK_ENV')

        print(environment)

        if environment == 'local':
            load_dotenv(dotenv_path='.env.local')
        elif environment == 'test':
            load_dotenv(dotenv_path='.env.test')
        else:
            load_dotenv(dotenv_path='.env')

        self.ENVIRONMENT = environment
        self.APP_NAME=os.getenv('APP_NAME')
        self.URL_REPORTS_SERVICE=os.getenv('URL_REPORTS_SERVICE')
        self.URL_ISSUES_SERVICE= os.getenv('URL_ISSUES_SERVICE')