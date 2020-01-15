from flask import Flask, jsonify, request
from src.search.entity_search import search_entities
from src.generator.questions_generator import generate_questions

app = Flask(__name__)


@app.route('/')
def index():
    return 'Server Works!'


@app.route('/search/<label>/')
def search_entities_by_label(label):
    """
    Endpoint for searching entities given a label.
    :param label: string representing a label in natural language.
    :return: entities with their associated identifiers.
    """
    entities = search_entities(label)
    return jsonify(entities)


@app.route('/entity/<entity_id>/')
def get_questions(entity_id):
    """
    Endpoint for obtaining questions about a given entity.
    :param entity_id: (Wikidata) Identifier for the entity used to generate the questions.
    :return: json file containing an array of question objects.
    """
    category = request.args.get('category')
    mcq = generate_questions(entity_id, questions_category=category)
    return jsonify(mcq)
