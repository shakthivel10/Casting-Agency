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
    @requires_auth("get:actor")
    def get_actors(jwt):

        query_result = Actor.query.all()
        response = []

        for obj in query_result:
            actor = obj.format()
            movies = []
            for casted_in in obj.casted_in:
                movies.append(casted_in.movie.title)
            actor["movies"] = movies
            response.append(actor)

        return jsonify(response)

    @app.route('/movies', methods=["GET"])
    @requires_auth("get:movie")
    def get_movies(jwt):
        query_result = Movie.query.all()
        response = []

        for obj in query_result:
            movie = obj.format()
            actors = []
            for casted in obj.casted:
                actors.append(casted.actor.name)
            movie["actors"] = actors
            response.append(movie)

        return jsonify(response)

    @app.route('/actors/<id>', methods=["DELETE"])
    @requires_auth("delete:actor")
    def delete_actor(jwt, id=id):

        actor = Actor.query.filter(Actor.id == id).first()

        if not actor:
            abort(404)

        try:
            actor.delete()
            return (jsonify({"success": True,
                             "delete": id}), 200)
        except:
            print(sys.exc_info())
            abort(422)

    @app.route('/movies/<id>', methods=["DELETE"])
    @requires_auth("delete:movie")
    def delete_movie(jwt, id=id):

        movie = Movie.query.filter(Movie.id == id).first()

        if not movie:
            abort(404)

        try:
            movie.delete()
            return (jsonify({"success": True,
                             "delete": id}), 200)
        except:
            print(sys.exc_info())
            abort(422)

    @app.route("/actors", methods=["POST"])
    @requires_auth("post:actor")
    def post_actor(jwt):
        print(request.json)
        try:
            if "name" in request.json:
                name = request.json["name"]
            if "age" in request.json:
                age = request.json["age"]
            if "gender" in request.json:
                gender = request.json["gender"]

            new_actor = Actor(name=name, age=age, gender=gender)

            new_actor.insert()

            return (jsonify({"success": True,
                             "actor": new_actor.format()}), 200)

        except:
            print(sys.exc_info())
            abort(422)

    @app.route("/movies", methods=["POST"])
    @requires_auth("post:movie")
    def post_movie(jwt):
        print("here2")
        print(sys.exc_info())
        print(request.json)
        print(sys.exc_info())
        try:
            new_movie = Movie()
            print(request.json)
            if "title" in request.json:
                title = request.json["title"]
                new_movie.title = title
            if "release_date" in request.json:
                date_arr = [int(val)
                            for val in request.json["release_date"].split("-")]
                release_date = datetime.datetime(*date_arr)
                new_movie.release_date = release_date

            new_movie.insert()

            return (jsonify({"success": True,
                             "movie": new_movie.format()}), 200)

        except:
            print(sys.exc_info())
            abort(422)

    @app.route("/actors/<id>", methods=["PATCH"])
    @requires_auth("patch:actor")
    def patch_actor(jwt, id=id):

        actor = Actor.query.filter(Actor.id == id).first()
        if not actor:
            abort(404)

        try:
            if "name" in request.json:
                name = request.json["name"]
                actor.name = name
            if "age" in request.json:
                age = request.json["age"]
                actor.age = age
            if "gender" in request.json:
                gender = request.json["gender"]
                actor.gender = gender

            actor.update()

            return (jsonify({"success": True,
                             "actor": actor.format()}), 200)

        except:
            print(sys.exc_info())
            abort(422)

    @app.route("/movies/<id>", methods=["PATCH"])
    @requires_auth("patch:movie")
    def patch_movie(jwt, id=id):

        movie = Movie.query.filter(Movie.id == id).first()

        if not movie:
            abort(404)

        try:
            if "title" in request.json:
                title = request.json["title"]
                movie.title = title
            if "release_date" in request.json:
                date_arr = [int(val)
                            for val in request.json["release_date"].split("-")]
                release_date = datetime.datetime(*date_arr)
                movie.release_date = release_date

            movie.update()

            return (jsonify({"success": True,
                             "movie": movie.format()}), 200)

        except:
            print(sys.exc_info())
            abort(422)

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

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
