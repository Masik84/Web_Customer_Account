from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate

def create_app():

    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    return app