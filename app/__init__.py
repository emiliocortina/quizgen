from flask import Flask, jsonify, request
from flask_cors import CORS

from app.exceptions.invalid_usage import InvalidUsage
from app.search.entity_search import search_entities
from app.generator.questions_generator import generate_questions


def create_app():
    app = Flask(__name__)
    CORS(app)

    @app.route('/')
    def index():
        return 'Server Works!'

    @app.route('/search/entities.json')
    def search_entities_by_label():
        """
        Endpoint for searching entities given a label.
        :return: entities with their associated identifiers.
        """
        label = request.args.get('label')
        if label is None or len(label.strip()) == 0:
            raise InvalidUsage('Please enter the label.', status_code=404)
        lang = request.args.get('lang')
        entities = search_entities(label, lang)
        return jsonify(entities)

    @app.route('/generate/questions.json')
    def get_questions():
        """
        Endpoint for obtaining questions about a given entity.
        :return: json file containing an array of question objects.
        """
        entity = request.args.get('entity')
        if entity is None:
            raise InvalidUsage('Please enter an identifier for the entity', status_code=404)
        category = request.args.get('category')
        if category is None:
            raise InvalidUsage('Please enter an identifier for the category template', status_code=404)
        limit = request.args.get('limit')
        lang = request.args.get('lang')
        mcq = generate_questions(entity, questions_category=category, questions_limit=limit, language=lang)
        return jsonify(mcq)

    @app.errorhandler(InvalidUsage)
    def handle_invalid_usage(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    return app
