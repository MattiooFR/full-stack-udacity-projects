import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    formatted_questions = [question.format() for question in selection]
    current_questions = formatted_questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    cors = CORS(app, resources={r"/*": {"origins": "*"}})

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response

    @app.route('/categories', methods=['GET'])
    def retrieve_categories():
        categories = Category.query.all()
        formatted_categories = {}

        for category in categories:
            formatted_categories[category.id] = category.type

        return jsonify({
            'success': True,
            'categories': formatted_categories
        })

    @app.route('/questions', methods=['GET', 'POST'])
    def get_questions():
        body = request.get_json()

        if request.method == "POST":
            search_term = body.get("searchTerm")
            if search_term is not None:
                search_term = f"%{search_term}%"
                questions = Question.query.filter(
                    Question.question.ilike(search_term)).all()
                formatted_questions = paginate_questions(request, questions)
                current_category = None

                if (len(questions) > 0):
                    current_category = Category.query.get(
                        questions[0].category).format()

                return jsonify({
                    'success': True,
                    'questions': formatted_questions,
                    'currentCategory': current_category,
                    'totalQuestions': len(questions)
                })
            else:
                question = body.get("question")
                answer = body.get("answer")
                category = body.get("category")
                difficulty = body.get("difficulty")

                # I think it should be validated in the form not here
                if(answer == '' or question == '' or answer is None or question is None):
                    abort(400)

                question = Question(question=question, answer=answer,
                                    category=category, difficulty=difficulty)
                try:
                    question.insert()
                    return jsonify({
                        "success": True,
                        'question_id': question.id
                    }), 200
                except:
                    abort(422)
        else:
            questions = Question.query.all()
            categories = Category.query.all()
            formatted_questions = paginate_questions(request, questions)
            formatted_categories = {}
            current_category = None

            if (len(formatted_questions) > 0):
                current_category = Category.query.get(
                    questions[0].category).format()
            else:
                abort(404)

            for category in categories:
                formatted_categories[category.id] = category.type

            return jsonify({
                'success': True,
                'questions': formatted_questions,
                'categories': formatted_categories,
                'currentCategory': current_category,
                'total_questions': len(questions)
            })

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()

            if question is None:
                abort(422)

            question.delete()

            return jsonify({
                'success': True
            })

        except:
            abort(422)

    @app.route("/category/<int:category_id>")
    def filter_by_category(category_id):
        category = Category.query.get(category_id)
        if category is None:
            abort(422)

        questions = Question.query.filter_by(category=category_id).all()
        formatted_questions = paginate_questions(request, questions)

        return jsonify({
            'success': True,
            'questions': formatted_questions,
            'currentCategory': category.format(),
            'totalQuestions': len(questions)
        })

    @app.route("/quizzes", methods=['POST'])
    def get_quizz_questions():
        try:
            body = request.get_json()

            previous_questions = body.get('previous_questions', None)
            category = body.get('quiz_category', None)

            if (category is None or category['id'] == 0):
                next_question = Question.query.filter(
                    ~Question.id.in_(previous_questions)).first()
            else:
                next_question = Question.query.filter_by(category=category['id']).filter(
                    ~Question.id.in_(previous_questions)).first()

            return jsonify({
                'success': True,
                'question': next_question.format()
            })
        except:
            abort(422)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    return app
