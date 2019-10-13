# selectedKey = keys[0]
#
# if(selectedKey is not None):
#     # Getting the entity
#

from flask import Flask, jsonify
from theme_selector import EntitySelector
from wikidata.client import Client

app = Flask(__name__)


@app.route('/')
def index():
    return 'Server Works!'

#adding variables
@app.route('/search/<label>')
def searchEntities(label):
  #returns the username
  selector = EntitySelector()
  entities = selector.searchEntities(label)
  return jsonify(entities)

@app.route('/entity/<entityID>')
def say_hello(entityID):
    client = Client()  # doctest: +SKIP
    entity = client.get(entityID, load=True)
    print('Selected entity info: ')
    print(entity)
    return str(entity)
