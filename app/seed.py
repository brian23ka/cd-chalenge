from app import create_app, db
from app.models import Hero, Power, HeroPower

app = create_app()

with app.app_context():
    db.create_all()

    if Hero.query.count() == 0:
        heroes = [
            Hero(name="Kamala Khan", super_name="Ms. Marvel"),
            Hero(name="Doreen Green", super_name="Squirrel Girl"),
            Hero(name="Gwen Stacy", super_name="Spider-Gwen"),
            Hero(name="Janet Van Dyne", super_name="The Wasp"),
            Hero(name="Wanda Maximoff", super_name="Scarlet Witch"),
            Hero(name="Carol Danvers", super_name="Captain Marvel"),
            Hero(name="Jean Grey", super_name="Dark Phoenix"),
            Hero(name="Ororo Munroe", super_name="Storm"),
            Hero(name="Kitty Pryde", super_name="Shadowcat"),
            Hero(name="Elektra Natchios", super_name="Elektra"),
        ]
        db.session.add_all(heroes)
        db.session.commit()
        print("Heroes seeded.")

    if Power.query.count() == 0:
        powers = [
            Power(name="super strength", description="gives the wielder super-human strengths"),
            Power(name="flight", description="gives the wielder the ability to fly through the skies at supersonic speed"),
            Power(name="super human senses", description="allows the wielder to use her senses at a super-human level"),
            Power(name="elasticity", description="can stretch the human body to extreme lengths"),
        ]
        db.session.add_all(powers)
        db.session.commit()
        print("Powers seeded.")

    if HeroPower.query.count() == 0:
        # Example associations (some random ones)
        associations = [
            HeroPower(hero_id=1, power_id=1, strength="Strong"),
            HeroPower(hero_id=1, power_id=2, strength="Strong"),
            HeroPower(hero_id=2, power_id=3, strength="Average"),
            HeroPower(hero_id=3, power_id=1, strength="Weak"),
        ]
        db.session.add_all(associations)
        db.session.commit()
        print("HeroPowers seeded.")
