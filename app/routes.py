from flask import request, jsonify
from flask_restful import Resource
from flask_mail import Message
from .models import db, Hero, Power, HeroPower
from . import mail

class IndexResource(Resource):
    def get(self):
        return {"message": "API is running"}

class HeroesResource(Resource):
    def get(self):
        heroes = Hero.query.all()
        return [{"id": h.id, "name": h.name, "super_name": h.super_name} for h in heroes], 200

class HeroResource(Resource):
    def get(self, id):
        hero = Hero.query.get(id)
        if not hero:
            return {"error": "Hero not found"}, 404
        return {
            "id": hero.id,
            "name": hero.name,
            "super_name": hero.super_name,
            "hero_powers": [
                {
                    "id": hp.id,
                    "hero_id": hp.hero_id,
                    "power_id": hp.power_id,
                    "strength": hp.strength,
                    "power": {
                        "id": hp.power.id,
                        "name": hp.power.name,
                        "description": hp.power.description
                    }
                } for hp in hero.hero_powers
            ]
        }, 200

class PowersResource(Resource):
    def get(self):
        powers = Power.query.all()
        return [
            {"id": p.id, "name": p.name, "description": p.description}
            for p in powers
        ], 200

class PowerResource(Resource):
    def get(self, id):
        power = Power.query.get(id)
        if not power:
            return {"error": "Power not found"}, 404
        return {
            "id": power.id,
            "name": power.name,
            "description": power.description
        }, 200

    def patch(self, id):
        power = Power.query.get(id)
        if not power:
            return {"error": "Power not found"}, 404
        data = request.get_json()
        description = data.get("description")
        errors = []
        if not description or len(description) < 20:
            errors.append("Description must be present and at least 20 characters long")
        if errors:
            return {"errors": errors}, 400
        power.description = description
        db.session.commit()
        return {
            "id": power.id,
            "name": power.name,
            "description": power.description
        }, 200

class HeroPowersResource(Resource):
    def post(self):
        data = request.get_json()
        strength = data.get("strength")
        power_id = data.get("power_id")
        hero_id = data.get("hero_id")
        errors = []
        if strength not in ["Strong", "Weak", "Average"]:
            errors.append("Strength must be 'Strong', 'Weak', or 'Average'")
        if not power_id or not hero_id:
            errors.append("power_id and hero_id are required")
        power = Power.query.get(power_id)
        hero = Hero.query.get(hero_id)
        if not power:
            errors.append("Power not found")
        if not hero:
            errors.append("Hero not found")
        if errors:
            return {"errors": errors}, 400
        hero_power = HeroPower(strength=strength, power_id=power_id, hero_id=hero_id)
        db.session.add(hero_power)
        db.session.commit()
        return {
            "id": hero_power.id,
            "hero_id": hero_power.hero_id,
            "power_id": hero_power.power_id,
            "strength": hero_power.strength,
            "hero": {
                "id": hero.id,
                "name": hero.name,
                "super_name": hero.super_name
            },
            "power": {
                "id": power.id,
                "name": power.name,
                "description": power.description
            }
        }, 201

class SendTestEmailResource(Resource):
    def post(self):
        data = request.get_json()
        recipient = data.get('recipient')
        if not recipient:
            return {"error": "Recipient email required"}, 400
        msg = Message(
            subject="Superheroes API Test Email",
            sender="your_email@gmail.com",
            recipients=[recipient],
            body="This is a test email from your Superheroes API."
        )
        mail.send(msg)
        return {"message": f"Email sent to {recipient}"}, 200

def register_resources(api):
    api.add_resource(IndexResource, '/')
    api.add_resource(HeroesResource, '/heroes')
    api.add_resource(HeroResource, '/heroes/<int:id>')
    api.add_resource(PowersResource, '/powers')
    api.add_resource(PowerResource, '/powers/<int:id>')
    api.add_resource(HeroPowersResource, '/hero_powers')
    api.add_resource(SendTestEmailResource, '/send_test_email')
