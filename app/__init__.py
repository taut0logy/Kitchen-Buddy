from flask import Flask
from app.routes import api
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.register_blueprint(api, url_prefix='/api')
    return app
