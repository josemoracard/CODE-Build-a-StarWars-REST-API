"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Characters, Planets, Favorite_Characters, Favorite_Planets
#from models import Person
import requests

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/users', methods=['GET'])
def get_users():
    get_all_users = User.query.all()
    get_all_users = list(map(lambda x: x.serialize(), get_all_users))
    return jsonify(get_all_users), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    data = request.get_json()
    new_favorite_planet = Favorite_Planets(user_id=data["user_id"], planet_id=planet_id)
    db.session.add(new_favorite_planet)
    db.session.commit()
    return jsonify("Tu planeta se ha añadido correctamente."), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def remove_favorite_planet(planet_id):
    data = request.get_json()
    planet = Favorite_Planets.query.filter_by(user_id=data["user_id"], planet_id=planet_id).first()
    db.session.delete(planet)
    db.session.commit()
    return jsonify("Planeta borrado correctamente."), 200

@app.route('/favorite/characters/<int:character_id>', methods=['POST'])
def add_favorite_character(character_id):
    data = request.get_json()
    new_favorite_character = Favorite_Characters(user_id=data["user_id"], character_id=character_id)
    db.session.add(new_favorite_character)
    db.session.commit()
    return jsonify("Tu personaje se ha añadido correctamente."), 200

@app.route('/favorite/character/<int:character_id>', methods=['DELETE'])
def remove_favorite_character(character_id):
    data = request.get_json()
    character = Favorite_Characters.query.filter_by(user_id=data["user_id"], character_id=character_id).first()
    db.session.delete(character)
    db.session.commit()
    return jsonify("Personaje borrado correctamente."), 200

@app.route('/people', methods=['GET'])
def handle_people():
    get_all_people = Characters.query.all()
    get_all_people = list(map(lambda x: x.serialize(), get_all_people))
    return jsonify(get_all_people), 200

@app.route('/planets', methods=['GET'])
def handle_planets():
    get_all_planets = Planets.query.all()
    get_all_planets = list(map(lambda x: x.serialize(), get_all_planets))
    return jsonify(get_all_planets), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
