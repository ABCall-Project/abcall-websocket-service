from flask_restful import Resource, Api
from flask import Flask, request, json
from .utils.json_custom_encoder import JSONCustomEncoder
import requests
from flaskr import create_app
from config import Config
from .endpoint import HealthCheck

config = Config()


app = create_app('default')
app.json_encoder = JSONCustomEncoder

app_context = app.app_context()
app_context.push()


api = Api(app)

#resources
api.add_resource(HealthCheck, '/health')