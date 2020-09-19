import os
import sys
import json
import datetime
from flask import Flask, request, Response, abort, jsonify
from werkzeug.datastructures import MultiDict
from models import setup_db, db_drop_and_create_all, Actor, Movie, CastedIn
from flask_cors import CORS, cross_origin


def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    cors = CORS(app)

    db_drop_and_create_all()

    a1 = Actor(name="A", age=30, gender="Male")
    a1.insert()

    m1 = Movie(title="M", release_date=datetime.datetime(2020, 9, 18))
    m1.insert()

    c1 = CastedIn(actor_id=1, movie_id=1)
    c1.insert()

    @app.route('/')
    def index():
        return jsonify("Healthy!")

    @app.route('/actors', methods=["GET"])
    def get_actors():

        query_result = Actor.query.all()
        actors = []

        for obj in query_result:
            actor = obj.format()
            movies = []
            for casted_in in obj.casted_in:
                movies.append(casted_in.movie.title)
            actor["movies"] = movies
            actors.append(actor)

        return jsonify(actors)

    @app.route('/movies', methods=["GET"])
    def get_movies():
        query_result = Movie.query.all()
        movies = []

        for obj in query_result:
            movie = obj.format()
            actors = []
            for casted in obj.casted:
                actors.append(casted.actor.name)
            movie["actors"] = actors
            movies.append(movie)

        return jsonify(movies)

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
