from app import db
from sqlalchemy.dialects.postgresql import json
from sqlalchemy.orm import  relationship
from flask_jwt_extended import create_access_token
from datetime import timedelta
import bcrypt


class Region(db.Model):
    __tablename__ = 'region'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    relation_id = relationship('Town')

    def _init__(self, name):
        self.name = name


class Town(db.Model):
    __tablename__ = 'town'

    id = db.Column(db.Integer, primary_key=True)
    town_name = db.Column(db.String(50), nullable=False)

    region_id = db.Column(db.Integer, db.ForeignKey('region.id'))

    def __init__(self, town_name, region_id):
        self.town_name = town_name
        self.region_id = region_id

    def __repr__(self):
        return f"{self.id=} { self.town_name=} {self.region_id=}"


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(password=password.encode('utf-8'), salt=bcrypt.gensalt())

    def __repr__(self):
        return f"{self.id=} {self.name=} {self.email=} {self.password=}"

    def get_token(self, expire_time=24):
        expire_delta = timedelta(expire_time)
        token = create_access_token(identity=self.id, expires_delta=expire_delta)
        return token

    @classmethod
    def authenticate(cls, email, password):
        user = db.session.query(cls).filter(cls.email == email).first()
        if not bcrypt.checkpw(password.encode('utf-8'), user.password):
            raise Exception("No user with this password")
        return user