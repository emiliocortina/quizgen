# selectedKey = keys[0]
#
# if(selectedKey is not None):
#     # Getting the entity
#

from flask import Flask, jsonify, request
from tfg.search.entity_search import search_entities
from tfg.generator.questions_generator import generateQuestions

app = Flask(__name__)


@app.route('/')
def index():
    return 'Server Works!'

#adding variables
@app.route('/search/<label>/')
def searchEntities(label):
  #returns the username
  entities = search_entities(label)
  return jsonify(entities)

#adding variables
@app.route('/hello/<label>/')
def helloLabel(label):
  #returns the username
  predefined_string = '%s is the mayor of Madrid'
  return (predefined_string%(label))

@app.route('/entity/<entity_id>/')
def say_hello(entity_id,):
    category = request.args.get('category')
    mcq = generateQuestions(entity_id, questions_category=category)
    return jsonify(mcq)
