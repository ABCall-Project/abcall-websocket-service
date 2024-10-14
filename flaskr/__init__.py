from flask import Flask
from datetime import timedelta


def create_app(config_name):
    app = Flask(__name__)
    return app

from .app import *