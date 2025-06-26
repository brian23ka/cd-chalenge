from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_restful import Api

db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
api = Api()

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'your_email@gmail.com'
    app.config['MAIL_PASSWORD'] = 'your_app_password'  # Use an app password, not your real password!

    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    api.init_app(app)

    from .routes import register_resources
    register_resources(api)

    return app

# For compatibility with run.py
app = create_app()
