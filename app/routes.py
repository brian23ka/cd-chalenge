from flask import Blueprint, request, jsonify
from .models import db, Hero, Power, HeroPower

api = Blueprint('api', __name__)

@api.route('/')
def index():
    return {"message": "API is running"}

# GET /heroes
@api.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    return jsonify([{"id": h.id, "name": h.name, "super_name": h.super_name} for h in heroes]), 200

# GET /heroes/<int:id>
@api.route('/heroes/<int:id>', methods=['GET'])
def get_hero(id):
    hero = Hero.query.get(id)
    if not hero:
        return jsonify({"error": "Hero not found"}), 404
    return jsonify({
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
    }), 200

# GET /powers
@api.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    return jsonify([
        {"id": p.id, "name": p.name, "description": p.description}
        for p in powers
    ]), 200

# GET /powers/<int:id>
@api.route('/powers/<int:id>', methods=['GET'])
def get_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({"error": "Power not found"}), 404
    return jsonify({
        "id": power.id,
        "name": power.name,
        "description": power.description
    }), 200

# PATCH /powers/<int:id>
@api.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({"error": "Power not found"}), 404
    data = request.get_json()
    description = data.get("description")
    errors = []
    if not description or len(description) < 20:
        errors.append("Description must be present and at least 20 characters long")
    if errors:
        return jsonify({"errors": errors}), 400
    power.description = description
    db.session.commit()
    return jsonify({
        "id": power.id,
        "name": power.name,
        "description": power.description
    }), 200

# POST /hero_powers
@api.route('/hero_powers', methods=['POST'])
def create_hero_power():
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
        return jsonify({"errors": errors}), 400
    hero_power = HeroPower(strength=strength, power_id=power_id, hero_id=hero_id)
    db.session.add(hero_power)
    db.session.commit()
    return jsonify({
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
    }), 201
