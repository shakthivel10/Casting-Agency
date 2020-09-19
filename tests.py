import os
import unittest
import json

from app import create_app
from models import setup_db, Movie, Actor
from flask_sqlalchemy import SQLAlchemy


class AppTestCases(unittest.TestCase):
    """This class represents the test cases"""

    def setUp(self):
        """Define test variables and initialize app."""

        self.casting_assistant_request_header = {
            "Authorization": "Bearer "+os.environ['CASTING_ASSISTANT_TOKEN']
        }
        self.casting_director_request_header = {
            "Authorization": "Bearer "+os.environ['CASTING_DIRECTOR_TOKEN']
        }
        self.casting_producer_request_header = {
            "Authorization": "Bearer "+os.environ['CASTING_PRODUCER_TOKEN']
        }

        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.environ['LOCAL_TEST_DB_URL']
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables if not already present
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_retrieve_actors(self):
        response = self.client().get('/actors', headers=self.casting_producer_request_header)
        response_data = json.loads(response.data)

        actor_query_result = Actor.query.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_data), len(actor_query_result))

    def test_retrieve_actors_error(self):
        response = self.client().get('/actors')

        self.assertEqual(response.status_code, 401)

    def test_retrieve_movies(self):
        response = self.client().get('/movies', headers=self.casting_producer_request_header)
        response_data = json.loads(response.data)

        movie_query_result = Movie.query.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_data), len(movie_query_result))

    def test_retrieve_movies_error(self):
        response = self.client().get('/movies')

        self.assertEqual(response.status_code, 401)

    def test_create_new_actor(self):
        prev_count = Actor.query.count()
        request_data = {"name": "keanu reeves", "age": "56", "gender": "male"}

        response = self.client().post("/actors", json=request_data,
                                      headers=self.casting_producer_request_header)

        self.assertEqual(response.status_code, 200)

        currrent_count = Actor.query.count()
        self.assertEqual(currrent_count, prev_count+1)

    def test_create_new_actor_error(self):
        response = self.client().post("/actors", headers=self.casting_producer_request_header)

        self.assertEqual(response.status_code, 400)

    def test_create_new_movie(self):
        prev_count = Movie.query.count()
        request_data = {"titile": "the matrix", "release_date": "1999-03-31"}

        response = self.client().post("/movies", json=request_data,
                                      headers=self.casting_producer_request_header)

        self.assertEqual(response.status_code, 200)

        currrent_count = Movie.query.count()
        self.assertEqual(currrent_count, prev_count+1)

    def test_create_new_movie_error(self):
        response = self.client().post("/movies", headers=self.casting_producer_request_header)

        self.assertEqual(response.status_code, 400)

    def test_update_new_actor(self):
        request_data = {"age": "57"}
        actor = Actor.query.first()

        if actor:
            to_update_id = actor.id
            response = self.client().patch("/actors/"+str(to_update_id), json=request_data,
                                           headers=self.casting_producer_request_header)
            self.assertEqual(response.status_code, 200)

    def test_update_new_actor_error(self):

        response = self.client().patch("/actors/1",
                                       headers=self.casting_producer_request_header)

        self.assertEqual(response.status_code, 400)

    def test_update_new_movie(self):
        request_data = {"release_date": "2021-12-12"}
        movie = Movie.query.first()

        if movie:
            to_update_id = movie.id
            response = self.client().patch("/movies/"+str(to_update_id), json=request_data,
                                           headers=self.casting_producer_request_header)
            self.assertEqual(response.status_code, 200)

    def test_update_new_movie_error(self):

        response = self.client().patch("/movies/1",
                                       headers=self.casting_producer_request_header)

        self.assertEqual(response.status_code, 400)

    def test_delete_actor(self):
        actor = Actor.query.first()

        if actor:
            to_delete_id = actor.id
            response = self.client().delete('/actors/' + str(to_delete_id),
                                            headers=self.casting_producer_request_header)
            self.assertEqual(response.status_code, 200)

            count = Actor.query.filter(Actor.id == to_delete_id).count()
            self.assertEqual(count, 0)

    def test_delete_actor_error(self):
        actor = Actor.query.first()

        if actor:
            to_delete_id = actor.id
            response = self.client().delete('/actors/' + str(to_delete_id))
            self.assertEqual(response.status_code, 401)

    def test_delete_movie(self):
        movie = Movie.query.first()

        if movie:
            to_delete_id = movie.id
            response = self.client().delete('/movies/' + str(to_delete_id),
                                            headers=self.casting_producer_request_header)
            self.assertEqual(response.status_code, 200)

            count = Movie.query.filter(Movie.id == to_delete_id).count()
            self.assertEqual(count, 0)

    def test_delete_movie_error(self):
        movie = Movie.query.first()

        if movie:
            to_delete_id = movie.id
            response = self.client().delete('/movies/' + str(to_delete_id))

            self.assertEqual(response.status_code, 401)

    def test_assistant_role(self):
        response = self.client().get('/actors', headers=self.casting_assistant_request_header)
        response_data = json.loads(response.data)

        actor_query_result = Actor.query.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_data), len(actor_query_result))

    def test_assistant_role_error(self):
        response = self.client().delete(
            '/actors/1', headers=self.casting_assistant_request_header)

        self.assertEqual(response.status_code, 401)

    def test_director_role(self):
        prev_count = Actor.query.count()
        request_data = {"name": "Tom Hanks", "age": "64", "gender": "male"}

        response = self.client().post("/actors", json=request_data,
                                      headers=self.casting_director_request_header)

        self.assertEqual(response.status_code, 200)

        currrent_count = Actor.query.count()
        self.assertEqual(currrent_count, prev_count+1)

    def test_director_role_error(self):
        prev_count = Movie.query.count()
        request_data = {"titile": "Forrest Gump", "release_date": "1994-07-06"}

        response = self.client().post("/movies", json=request_data,
                                      headers=self.casting_director_request_header)

        self.assertEqual(response.status_code, 401)

    def test_producer_role(self):
        prev_count = Movie.query.count()
        request_data = {"titile": "Forrest Gump", "release_date": "1994-07-06"}

        response = self.client().post("/movies", json=request_data,
                                      headers=self.casting_producer_request_header)

        self.assertEqual(response.status_code, 200)

        currrent_count = Movie.query.count()
        self.assertEqual(currrent_count, prev_count+1)

    def test_producer_role_error(self):
        response = self.client().get('/movie', headers=self.casting_producer_request_header)

        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
