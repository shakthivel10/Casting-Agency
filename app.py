import os
import sys
import json
import datetime
from flask import Flask, request, Response, abort, jsonify
from werkzeug.datastructures import MultiDict
from models import setup_db, db_drop_and_create_all, Actor, Movie, CastedIn
from flask_cors import CORS, cross_origin
from auth import AuthError, requires_auth


def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    cors = CORS(app)

    # db_drop_and_create_all()

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

# Error Handling


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "not found"
    }), 404


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
    }), 400


@app.errorhandler(409)
def conflict(error):
    return (jsonify({"success": False,
                     "error": 409,
                     "message": "A drink with the same title already exists"}),
            409)


@app.errorhandler(AuthError)
def auth_error(error):
    return (jsonify({
                    "success": False,
                    "error": error.status_code,
                    "message": error.error,
                    }), error.status_code)


app = create_app()

if __name__ == '__main__':
    app.run()
