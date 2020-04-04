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
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik56TTFRekF3UWpWRVJqRkRSamM1UlVFMk9ESTJOVUZGT0Rnek5qbEdNRFl5TnpBd1FqRXdNQSJ9.eyJpc3MiOiJodHRwczovL21hdHRpb28uZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlODg4ODZmNDQ3ZWZkMGJlMDczMzNiMyIsImF1ZCI6ImNvZmZlZXNob3AiLCJpYXQiOjE1ODYwMTQ3MTIsImV4cCI6MTU4NjAyMTkxMiwiYXpwIjoibzFremVHTFc5NEJRRXNXOTUxR1o3TEVZNE8yZEIzVDUiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDpkcmlua3MtZGV0YWlsIl19.X4OoW2ZeE7EgHkx8IHSg50cPTnSwmifApLqbg3XC9c8cOKOPrxlL_FSn5Lna-RU4FQDKOiS15iFkSVT0G4yt0Qji_0noF64fNfi5vp-b4ilgPDbNu5wrKpKT8c1lfI4Y5c0XXX8zPKPZXfgjyjybP38dyvYJj6gvAQCA0LL2tbxXDwGU8uBZkAGRFXcEbPN_wExiryuUMGD5nHFsLw3EQuSADJt_cmrT2rOpiNOG51Qm46zQtqfKBzhsXjQyhuPuo5jRl8n2MnKa_W4-E10d0hKjXwKhPsWRXuiX86HmhwI3bRRhRkIxVvDdl36qsWTMeg4fR8woVr059W-GZk0Lwg

manager@gmail.com
Manager81
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik56TTFRekF3UWpWRVJqRkRSamM1UlVFMk9ESTJOVUZGT0Rnek5qbEdNRFl5TnpBd1FqRXdNQSJ9.eyJpc3MiOiJodHRwczovL21hdHRpb28uZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlODg4OGI4NDQ3ZWZkMGJlMDczMzNlYiIsImF1ZCI6ImNvZmZlZXNob3AiLCJpYXQiOjE1ODYwMTQ3NTMsImV4cCI6MTU4NjAyMTk1MywiYXpwIjoibzFremVHTFc5NEJRRXNXOTUxR1o3TEVZNE8yZEIzVDUiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpkcmlua3MiLCJnZXQ6ZHJpbmtzLWRldGFpbCIsInBhdGNoOmRyaW5rcyIsInBvc3Q6ZHJpbmtzIl19.h7Bz3nJYANhoKUjSCVE9-nIdOydxFTmAIUYvwGZAGSO0Scc8dgro7oMJESPcHUbi62qjGV-jFBi43nXGUi_sbaYNglUBOdDdhnx6XmdT8V03-mnteovULuDfQknuiJGfyk7qZykJArJ5IRXSx2xtpLr6DGKluxuVAuGeLtPiscayLJTDqp5l9ioHpnK8YEe_zlh-ULcUWWnUzdRhUIpcS52gk9DKJXB5ao81SbY35yt3P1R6W4yfLBbpvj_tRaAvfANDAVT9MruFFZc4BbvY_9ovGCdjN7B6pPynyPXeoHJrmF3_R0Tedl3AN5DqEVHrTH2dNAYEXAzvkAm08W8AGw

### Implement The Server

There are `@TODO` comments throughout the `./backend/src`. We recommend tackling the files in order and from top to bottom:

1. `./src/auth/auth.py`
2. `./src/api.py`
