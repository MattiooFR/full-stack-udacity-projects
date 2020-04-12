# Coffee Shop Backend

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

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=api.py;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Tasks

### Setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
    - in API Settings:
        - Enable RBAC
        - Enable Add Permissions in the Access Token
5. Create new API permissions:
    - `get:drinks-detail`
    - `post:drinks`
    - `patch:drinks`
    - `delete:drinks`
6. Create new roles for:
    - Barista
        - can `get:drinks-detail`
    - Manager
        - can perform all actions
7. Test your endpoints with [Postman](https://getpostman.com).
    - Register 2 users - assign the Barista role to one and Manager role to the other.
    - Sign into each account and make note of the JWT.
    - Import the postman collection `./starter_code/backend/udacity-fsnd-udaspicelatte.postman_collection.json`
    - Right-clicking the collection folder for barista and manager, navigate to the authorization tab, and including the JWT in the token field (you should have noted these JWTs).
    - Run the collection and correct any errors.
    - Export the collection overwriting the one we've included so that we have your proper JWTs during review!

Login URL
https://mattioo.eu.auth0.com/authorize?audience=coffeeshop&response_type=token&client_id=o1kzeGLW94BQEsW951GZ7LEY4O2dB3T5&redirect_uri=http://localhost:8080/login-results

barista@gmail.com
Barista81
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik56TTFRekF3UWpWRVJqRkRSamM1UlVFMk9ESTJOVUZGT0Rnek5qbEdNRFl5TnpBd1FqRXdNQSJ9.eyJpc3MiOiJodHRwczovL21hdHRpb28uZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlODg4ODZmNDQ3ZWZkMGJlMDczMzNiMyIsImF1ZCI6ImNvZmZlZXNob3AiLCJpYXQiOjE1ODY3MDg1NzUsImV4cCI6MTU4NjcxNTc3NSwiYXpwIjoibzFremVHTFc5NEJRRXNXOTUxR1o3TEVZNE8yZEIzVDUiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDpkcmlua3MtZGV0YWlsIl19.Kbzgra8aZF3xS846VHAVe7TRmPyVfslKvdG6Hj4NyVbtNerIQTTR3QmCuvdssef2e0nhDpmukqPUAc2s-Hj2g7O10-F-eFqV6TkNSdB1Y-DgMe--NxgYyHts9Wa5dkgejVF-3BKCtZBrdJiy6HinzDs_4kkMFDct15GsZkK5fHuYRNFgMnA2GJE-Yfp3RsLMxLL4MvnXVaf2iiXP1YUZhzAtcQTolc9fy_2hbGT08QOwld80kg5kWj9QOJrrzP2HnRSrSeteCqPCl3oPOGGe_hyvP0VLVqn3u7jQhgsARc4dZOSTDshQi5cz_HzSqWWQgzrcihBrZ47036wp7RRi3A

manager@gmail.com
Manager81
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik56TTFRekF3UWpWRVJqRkRSamM1UlVFMk9ESTJOVUZGT0Rnek5qbEdNRFl5TnpBd1FqRXdNQSJ9.eyJpc3MiOiJodHRwczovL21hdHRpb28uZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlODg4OGI4NDQ3ZWZkMGJlMDczMzNlYiIsImF1ZCI6ImNvZmZlZXNob3AiLCJpYXQiOjE1ODY3MDg2MTcsImV4cCI6MTU4NjcxNTgxNywiYXpwIjoibzFremVHTFc5NEJRRXNXOTUxR1o3TEVZNE8yZEIzVDUiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpkcmlua3MiLCJnZXQ6ZHJpbmtzLWRldGFpbCIsInBhdGNoOmRyaW5rcyIsInBvc3Q6ZHJpbmtzIl19.hlNSq81n6D-a4bCmVtD5keTYyfDe8hEjfeqsesI4MIE6dZ9DOgZOeE47qA8Fb4OBuYxXEBYxGzXv-Z-AZY27NMZXCMlN5Kgm3JSTw7aPh4CGDhAEyJ0S8OXgG_qkZr0Bhl4EUgNgP4J6FGhUdX-n22bElmAh6JWX04x5bxHa4Jf1ldMDVY1RLHRl5Tgqnyzm9hJrQ9RDwA73eh52rajScelNQTyAwoLEZBJrYb1LS2zuxHmUF5n5QlbssZabyDcz-5IH3ogjm98_ochs7WjuRC4MRXpiI3TOMaU7qXMNNI04Z161b6pvLL1xTWj0iOgTJzTx1GqMc_nT5yMtK7pwMQ

### Implement The Server

There are `@TODO` comments throughout the `./backend/src`. We recommend tackling the files in order and from top to bottom:

1. `./src/auth/auth.py`
2. `./src/api.py`
