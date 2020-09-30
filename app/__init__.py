from flask import Flask
from config import config_options
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app(config_name):

  app = Flask(__name__)

  # Creating the app configurations
  app.config.from_object(config_options[config_name])

  # Initializing flask extensions
  db.init_app(app)
  login_manager.init_app(app)

  # Registering the blueprints
  from .main import main as main_blueprint
  app.register_blueprint(main_blueprint)

  from .auth import auth as auth_blueprint
  app.register_blueprint(auth_blueprint,url_prefix = '/authenticate')
  
  from .merchant import merchant as merchant_blueprint
  app.register_blueprint(merchant_blueprint,url_prefix = '/merchant')

  from .admin import admin as admin_blueprint
  app.register_blueprint(admin_blueprint,url_prefix = '/admin')

  from .clerk import clerk as clerk_blueprint
  app.register_blueprint(clerk_blueprint,url_prefix = '/clerk')

  
  return app