import os
import sys
import json
from flask import Flask, request, Response, abort, jsonify
from werkzeug.datastructures import MultiDict
from models import setup_db, Actor
from flask_cors import CORS, cross_origin


def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    cors = CORS(app)

    @app.route('/')
    def index():
        return jsonify("Hello World!")

    @app.route('/actors/<id>')
    def get_actors(id):
        result = Actor.query.filter(Actor.id == id).first()
        if result:
            return jsonify(result.format())
        else:
            abort(404)

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
