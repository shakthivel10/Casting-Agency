import os
import sys
from sqlalchemy import Column, String, create_engine
from flask_sqlalchemy import SQLAlchemy
import json


if sys.argv[0] == "tests.py":  # use local test database for running unit tests
    database_path = os.environ['LOCAL_TEST_DB_URL']
else:
    database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class CastedIn(db.Model):
    __tablename__ = 'casted_in'
    actor_id = Column(db.Integer, db.ForeignKey(
        'actor.id'), primary_key=True)
    movie_id = Column(db.Integer, db.ForeignKey(
        'movie.id'), primary_key=True)
    actor = db.relationship("Actor", back_populates="casted_in")
    movie = db.relationship("Movie", back_populates="casted")

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Actor(db.Model):
    __tablename__ = 'actor'

    id = Column(db.Integer, primary_key=True)
    name = Column(db.String)
    age = Column(db.Integer)
    gender = Column(db.String)
    casted_in = db.relationship('CastedIn', back_populates='actor')

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender}


class Movie(db.Model):
    __tablename__ = 'movie'

    id = Column(db.Integer, primary_key=True)
    title = Column(db.String)
    release_date = db.Column(db.DateTime())
    casted = db.relationship('CastedIn', back_populates='movie')

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date}
