from flask import Flask
import toml
from flask_wtf import CSRFProtect

#from flask_sqlalchemy import SQLAlchemy
from app.model.config import init_db

#db = SQLAlchemy()

def create_app(config_file):
    app = Flask(__name__, template_folder='../app/pages', static_folder='../app/resources')   
    app.config.from_file(config_file, toml.load)

# You're registering a function that runs 
# before every request to protected views.
    #csrf = CSRFProtect(app)

    #secret_key = app.config.get('SECRET_KEY')
    #app.secret_key = secret_key

    #init_db()

    #db.init_app(app)

    with app.app_context():
        from app.api import index
        from app.api.login import login

    return app
