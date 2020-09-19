# casting-agency
This project is a web application for a casting agency, whose goal is to find suitable actors to cast in different movies. It models relationships in SQLAlchemy ORM, implements RESTful APIs and enforces Role Based Access Control (RBAC) on the APIs using Auth0. This application is the capstone project of my Full Stack Web Developer Nanodegree Program. 

The App is hosted on heroku.  
URL: [https://web-app-casting-agency.herokuapp.com](https://web-app-casting-agency.herokuapp.com)

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 


### Running the server locally
1. Create a local Postgres database.
2. Create environment variable DATABASE_URL and set it to database URL.   
Example:
```bash
export DATABASE_URL=postgresql://$USER@localhost:5432/<your_db_name>
```

3. To run the server locally, execute:

```bash
source setup.sh
export FLASK_ENV=development
flask run
```

## APIs

### List of APIs 
GET '/actors'   
GET '/movies'  
POST '/actors'  
POST '/movies'  
PATCH '/actors/<int:id>'  
PATCH '/movies/<int:id>'   
DELETE '/actors/<int:id>'   
DELETE '/movies/<int:id>'   

All APIs are secured by RBAC, and are available depending on the user's role.  

### Roles and Accessible APIs

There are three roles: Casting Assistant, Casting Director and Casting Producer.
Each role has access to the followings APIs.

#### Casting Assistant  
GET '/actors'  
GET '/movies'  

#### Casting Director  
GET '/actors'   
GET '/movies'    
POST '/actors'    
PATCH '/actors/<int:id>'    
PATCH '/movies/<int:id>'    
DELETE '/actors/<int:id>'    

#### Casting Producer
GET '/actors'    
GET '/movies'    
POST '/actors'    
POST '/movies'    
PATCH '/actors/<int:id>'    
PATCH '/movies/<int:id>'    
DELETE '/actors/<int:id>'    
DELETE '/movies/<int:id>'    


### API Documentation

#### GET '/actors'
- Fetches a list of all actors in the database
- Request Arguments: None
- Returns: A list of actor objects, where each object has the following properties:  id, name, age, gender and list of movie titles the actor acted in.

Example Respone: GET '/actors'
``` 
[
    {
        "age": 45,
        "gender": "Male",
        "id": 1,
        "movies": [
            "Titanic",
            "Catch Me If You Can"
        ],
        "name": "Leonardo DiCaprio"
    },
    {
        "age": 44,
        "gender": "Female",
        "id": 2,
        "movies": [
            "Titanic"
        ],
        "name": "Kate Winslet"
    },
    {
        "age": 64,
        "gender": "Male",
        "id": 3,
        "movies": [
            "Forrest Gump",
            "Catch Me If You Can"
        ],
        "name": "Tom Hanks"
    },
    {
        "age": 54,
        "gender": "Female",
        "id": 4,
        "movies": [
            "Forrest Gump"
        ],
        "name": "Robin Wright"
    },
    {
        "age": 77,
        "gender": "Male",
        "id": 5,
        "movies": [
            "Catch Me If You Can"
        ],
        "name": "Christopher Walken"
    }
]
```

#### GET '/movies'
- Fetches a list of all movies in the database
- Request Arguments: None
- Returns: A list of movie objects, where each object has the following properties:  id, title, release_date and list of names of actors who acted in in the movie.

Example Respone: GET '/movies'
```
[
    {
        "actors": [
            "Tom Hanks",
            "Robin Wright"
        ],
        "id": 1,
        "release_date": "Wed, 06 Jul 1994 00:00:00 GMT",
        "title": "Forrest Gump"
    },
    {
        "actors": [
            "Leonardo DiCaprio",
            "Kate Winslet"
        ],
        "id": 2,
        "release_date": "Fri, 19 Dec 1997 00:00:00 GMT",
        "title": "Titanic"
    },
    {
        "actors": [
            "Leonardo DiCaprio",
            "Tom Hanks",
            "Christopher Walken"
        ],
        "id": 3,
        "release_date": "Wed, 25 Dec 2002 00:00:00 GMT",
        "title": "Catch Me If You Can"
    }
]
```

#### POST '/actors'
- Creates and inserts a new actor record into the database
- Request Body: actor information 
    { "name": <actor_name>, "age": <actor_age>, "gender": <actor_gender>}
- Returns: A JSON containing the actor inserted

Example Request: POST '/actors'
``` 
{
    "age": 77,
    "gender": "Male",
    "name": "Robert De Niro"
}
``` 
Response
```
{
    "actor": {
        "age": 77,
        "gender": "Male",
        "id": 9,
        "name": "Robert De Niro"
    },
    "success": true
}
```

#### POST '/movies'
- Creates and inserts a new movie record into the database
- Request Body: movie information 
    { "title": <movie_title>, "release_date": <<movie_release_date>}   
    The release date has to a string in the following format: "YYYY-MM-DD", example: “2021-12-31”
- Returns: A JSON containing the movie inserted

Example Request: POST '/movies'
``` 
{
    "release_date": "1976-02-08",
    "title": "Taxi Driver"
}
``` 
Response
```
{
    "movie": {
        "id": 6,
        "release_date": "Sun, 08 Feb 1976 00:00:00 GMT",
        "title": "Taxi Driver"
    },
    "success": true
}
```

#### PATCH '/actors/<int:id>'
- Updates an existing actor record in the database.
- Request Body: new actor information conatining one or more of the following keys 
    { "name": <actor_name>, "age": <actor_age>, "gender": <actor_gender>}
- Returns: A JSON containing the actor updated

Example Request: PATCH '/actors/1'
``` 
{
    "age":46
}
``` 
Response
```
{
    "actor": {
        "age": 46,
        "gender": "Male",
        "id": 1,
        "name": "Leonardo DiCaprio"
    },
    "success": true
}
```

#### PATCH '/movies/<int:id>'
- Updates an existing movie record in the database.
- Request Body: new movie information conatining one or more of the following keys 
    { "title": <movie_title>, "release_date": <<movie_release_date>}   
    The release date has to a string in the following format: "YYYY-MM-DD", example: “2021-12-31”
- Returns: A JSON containing the movie updated

Example Request: PATCH '/movies/1'
``` 
{
    "release_date":"1997-12-25"
}
``` 
Response:
```
{
    "movie": {
        "id": 1,
        "release_date": "Thu, 25 Dec 1997 00:00:00 GMT",
        "title": "Forrest Gump"
    },
    "success": true
}
```

#### DELETE '/actors/<int:id>'
- Deletes the actor with given id from the database
- Returns: the id of the actor succefully deleted

Example Request: DELETE '/actors/1'
Response:
```
{
    "delete": 1,
    "success": true
}
```

#### DELETE '/movies/<int:id>'
- Deletes the movie with given id from the database
- Returns: the id of the movie succefully deleted

Example Request: DELETE '/movies/1'
Response:
```
{
    "delete": 1,
    "success": true
}
```

## Login URL and Exisiting Accounts for different roles

The login URL is [https://dev-5d44q6nn.us.auth0.com/authorize?audience=cast&response_type=token&client_id=cH5mkmWqCV94th2fzUDwFDywFgg2VDaD&redirect_uri=https://web-app-casting-agency.herokuapp.com/actors](https://dev-5d44q6nn.us.auth0.com/authorize?audience=cast&response_type=token&client_id=cH5mkmWqCV94th2fzUDwFDywFgg2VDaD&redirect_uri=https://web-app-casting-agency.herokuapp.com/actors)

### Existing Accounts for different roles 

### Casting Assistant
#### username:  
castingassistant5786@gmail.com  
#### password:  
!castingassistant5786%

### Casting Director
#### username:  
castingdirector4132@gmail.com  
#### password:  
!castingdirector4132%  

### Casting Producer
#### username:  
castingproducer6879@gmail.com  
#### password:  
!castingproducer6879%  

## Testing
#### The unit tests are run locally.   
Instructions to run tests:
1. Create a local database for testing.
2. Import data from test_db.db  
For Example, if your test database is named casting_agency_test_db:
```bash
psql casting_agency_test_db < test_db.db 
```
3. Set “LOCAL_TEST_DB_URL“ to the db's url in your python virtual env.
Example:
```bash
export LOCAL_TEST_DB_URL=postgresql://$USER@localhost:5432/<test_database_name>
```
   
4. Import Environment Variables
```bash
source setup.sh
```
5. To run the tests
```
python tests.py
```

