from flask_restful import Resource, reqparse
from flask import jsonify, request
from app.models import Hero, Power, HeroPower
from app import db
from sqlalchemy.exc import IntegrityError

# Parsers

power_patch_parser = reqparse.RequestParser()
power_patch_parser.add_argument('description', type=str, required=True, help='Description is required and must be at least 20 characters.')

hero_power_post_parser = reqparse.RequestParser()
hero_power_post_parser.add_argument('strength', type=str, required=True, help="Strength is required and must be 'Strong', 'Weak' or 'Average'")
hero_power_post_parser.add_argument('power_id', type=int, required=True, help="power_id is required")
hero_power_post_parser.add_argument('hero_id', type=int, required=True, help="hero_id is required")


class HeroListResource(Resource):
    def get(self):
        heroes = Hero.query.all()
        return jsonify([hero.to_dict() for hero in heroes])


class HeroResource(Resource):
    def get(self, id):
        hero = Hero.query.get(id)
        if not hero:
            return {"error": "Hero not found"}, 404
        return jsonify(hero.to_dict_with_powers())


class PowerListResource(Resource):
    def get(self):
        powers = Power.query.all()
        return jsonify([power.to_dict() for power in powers])


class PowerResource(Resource):
    def get(self, id):
        power = Power.query.get(id)
        if not power:
            return {"error": "Power not found"}, 404
        return jsonify(power.to_dict())

    def patch(self, id):
        power = Power.query.get(id)
        if not power:
            return {"error": "Power not found"}, 404

        args = power_patch_parser.parse_args()
        description = args.get('description')

        # Validate description length here
        if not description or len(description) < 20:
            return {"errors": ["Description must be at least 20 characters long"]}, 400

        power.description = description

        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            return {"errors": ["validation errors"]}, 400

        return jsonify(power.to_dict())


class HeroPowerResource(Resource):
    def post(self):
        args = hero_power_post_parser.parse_args()
        strength = args.get('strength')
        power_id = args.get('power_id')
        hero_id = args.get('hero_id')

        # Validate strength
        if strength not in ['Strong', 'Weak', 'Average']:
            return {"errors": ["Strength must be one of: Strong, Weak, Average"]}, 400

        # Validate power and hero exist
        power = Power.query.get(power_id)
        hero = Hero.query.get(hero_id)
        if not power or not hero:
            return {"errors": ["Invalid hero_id or power_id"]}, 400

        hero_power = HeroPower(strength=strength, power=power, hero=hero)

        db.session.add(hero_power)
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            return {"errors": ["validation errors"]}, 400

        return jsonify(hero_power.to_dict_with_hero_power()), 201
