import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app, resources={r"*": {'origins': r"*"}})


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PUT,POST,DELETE')
    return response

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
db_drop_and_create_all()

## ROUTES

@app.route('/drinks', methods=['GET'])
def get_drinks():
    try:
        drinks = Drink.query.order_by(Drink.id).all()
        formatted_drinks = [drink.short_rep() for drink in drinks]

        return jsonify({"success": True, "drinks": formatted_drinks})
    except:
        abort(422)

@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_details(payload):
    try:
        drinks = Drink.query.all()
        formatted_drinks = [drinks.long_rep() for drink in drinks]

        return jsonify({"success": True, "drinks": formatted_drinks})
    except:
        abort(422)

@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink(payload):

    body = request.get_json()

    title = body.get('title', None)
    recipe = body.get('recipe', None)

    try:

        if None in (title, recipe):
            abort(400)

        drink = Drink(title=title, recipe=json.dumps(recipe))
        drink.insert()

        return jsonify({'success': True, 'drinks': [drink.long()]})
    except:
        abort(422)

@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(payload, drink_id):

    try:
        drink = Drink.query.filter_by(id=drink_id).one_or_none()

        if drink is None:
            abort(404)

        body = request.get_json()

        if 'title' in body:
            drink.title = body.get('title')

        if 'recipe' in body:
            drink.recipe = json.dump(body.get('recipe'))

        drink.update()

        return jsonify({'success': True, 'drinks': [drink.long()]})
    except:
        abort(422)

@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, drink_id):

    try:
        drink = Drink.query.filter(Drink.id == drink_id).one_or_none()

        if drink is None:
            abort(404)
        drink.delete()

        return jsonify({
            'success': True,
            'delete': drink.id
            })
    except:
        abort(422)

## Error Handling
@app.errorhandler(AuthError)
def auth_error(e):
    return (jsonify({
        'success': False,
        'error': e.status_code,
        'message': e.description
    }), e.status_code)

@app.errorhandler(400)
def bad_request(error):
    return (jsonify({
        'success': False,
        'error': 400,
        'message': 'Bad Request'
    }), 400)

@app.errorhandler(401)
def unauthorized(error):
    return (jsonify({
        'success': False,
        'error': 401,
        'message': 'Unauthorized'
    }), 401)

@app.errorhandler(404)
def not_found(error):
    return (jsonify({
        'success': False,
        'error': 404,
        'message': 'Resources Not Found'
    }), 404)

@app.errorhandler(405)
def not_allowed(error):
    return (jsonify({
        'success': False,
        'error': 405,
        'message': 'Method Not Allowed'
    }), 405)

@app.errorhandler(422)
def unprocessable(error):
    return (jsonify({
        'success': False,
        'error': 422,
        'message': 'Unprocessable'
    }), 422)

@app.errorhandler(500)
def internal_server_error(error):
    return (jsonify({
        'success': False,
        'error': 500,
        'message': 'Internal Server Error'
    }), 500)
