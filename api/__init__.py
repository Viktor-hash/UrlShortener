from flask_restx import Api
from flask import Flask
from .routes import ns

def create_api(app: Flask) -> Api:
    api = Api(app,
              version='1.0',
              title='URL Shortener API',
              description='A URL shortening API')
    api.add_namespace(ns)
    return api