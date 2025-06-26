from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)
    
    api = Api(app)

    from app.resources import (
        HeroListResource, HeroResource,
        PowerListResource, PowerResource,
        HeroPowerResource
    )

    api.add_resource(HeroListResource, '/heroes')
    api.add_resource(HeroResource, '/heroes/<int:id>')

    api.add_resource(PowerListResource, '/powers')
    api.add_resource(PowerResource, '/powers/<int:id>')

    api.add_resource(HeroPowerResource, '/hero_powers')

    # Error handler for 404 on /heroes/:id and /powers/:id
    @app.errorhandler(404)
    def not_found(e):
        return jsonify(error=str(e)), 404

    return app
