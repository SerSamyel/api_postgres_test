from flask import Flask, jsonify, request
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required

app = Flask(__name__)
app.config.from_object(Config)
jwt = JWTManager(app)

# for console test
client = app.test_client()

db = SQLAlchemy(app)

from models import *


@app.route('/region', methods=['GET'])
def get_region():
    regions = db.session.query(Region)
    serialised = []
    for region in regions:
        serialised.append({
            'id': region.id,
            'name': region.name
        })
    return jsonify(serialised)


@app.route('/region', methods=['POST'])
@jwt_required
def add_region():
    new_one = Region(**request.json)
    db.session.add(new_one)
    db.session.commit()
    serialised = ({
        'id': new_one.id,
        'name': new_one.name,
        'relation_id': new_one.relation_id}
    )
    return jsonify(serialised)


@app.route('/region/<int:region_id>', methods=['PUT'])
@jwt_required
def update_region(region_id):
    item = db.session.query(Region).filter(Region.id == region_id).first()
    params = request.json
    if not item:
        return {'message': 'No region with this id.'}, 400
    for key, value in params.items():
        setattr(item, key, value)
    db.session.commit()
    serialised = {
        'id': item.id,
        'name': item.name,
        'relation_id': item.relation_id}
    return serialised


@app.route('/region/<int:region_id>', methods=['DELETE'])
@jwt_required
def delete_region(region_id):
    item = db.session.query(Region).filter(Region.id == region_id).first()
    if not item:
        return {'message': 'No region with this id.'}, 400
    db.session.delete(item)
    db.session.commit()
    return '', 204


@app.route('/town/<int:region_id>', methods=['GET'])
def town(region_id):
    towns = db.session.query(Town).filter(Town.region_id == region_id)
    serialised = []
    for town in towns:
        serialised.append({
            'id': town.id,
            'town_name': town.town_name
        })
    return jsonify(serialised)


@app.route('/town', methods=['POST'])
@jwt_required
def add_town():
    new_one = Town(**request.json)
    db.session.add(new_one)
    db.session.commit()
    serialised = ({
        'id': new_one.id,
        'town_name': new_one.town_name,
        'region_id': new_one.region_id}
    )
    return jsonify(serialised)


@app.route('/town/<int:town_id>', methods=['PUT'])
@jwt_required
def update_town(town_id):
    item = db.session.query(Town).filter(Town.id == town_id).first()
    params = request.json
    if not item:
        return {'message': 'No town with this id.'}, 400
    for key, value in params.items():
        setattr(item, key, value)
    db.session.commit()
    serialised = {
        'id': item.id,
        'town_name': item.town_name,
        'region_id': item.region_id}
    return serialised


@app.route('/town/<int:town_id>', methods=['DELETE'])
@jwt_required
def delete_town(town_id):
    item = db.session.query(Town).filter(Town.id == town_id).first()
    if not item:
        return {'message': 'No region with this id.'}, 400
    db.session.delete(item)
    db.session.commit()
    return '', 204


@app.route('/register', methods=['POST'])
def register():
    params = request.json
    user = User(**params)
    db.session.add(user)
    db.session.commit()
    token = user.get_token()
    return {'access_token': token}


@app.route('/login', methods=['POST'])
def login():
    params = request.json
    user = User.authenticate(**params)
    token = user.get_token()
    return {'access_token': token}


if __name__ == '__main__':
    app.run()
