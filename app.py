# selectedKey = keys[0]
#
# if(selectedKey is not None):
#     # Getting the entity
#

from flask import Flask, jsonify
from tfg.selector.theme_selector import EntitySelector
from tfg.generator.mcq_generator import generateQuestions
from wikidata.client import Client

app = Flask(__name__)


@app.route('/')
def index():
    return 'Server Works!'

#adding variables
@app.route('/search/<label>/')
def searchEntities(label):
  #returns the username
  selector = EntitySelector()
  entities = selector.search_entities(label)
  return jsonify(entities)

#adding variables
@app.route('/hello/<label>/')
def helloLabel(label):
  #returns the username
  predefined_string = '%s is the mayor of Madrid'
  return (predefined_string%(label))

@app.route('/entity/<entityID>/')
def say_hello(entityID):
    mcq = generateQuestions(entityID)
    return mcq
