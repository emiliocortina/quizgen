import os
import requests
import json


def getEntityCategory(entity_id, locale="en"):
    entity_categories = getEntityCategories(entity_id, locale)
    basedir = os.path.abspath(os.path.dirname(__file__))
    data_file = os.path.join(basedir, 'templates/_index.json')
    with open(data_file) as json_file:
        available_categories = json.load(json_file)
        available_categories = set(available_categories)
        intersection = available_categories & entity_categories
        for category in intersection:
            return category


def getCategoryQuestions(category_id, locale="en"):
    basedir = os.path.abspath(os.path.dirname(__file__))
    data_file = os.path.join(basedir, 'templates/_index.json')
    with open(data_file) as json_categories:
        available_categories = json.load(json_categories)
        category_file = f'templates/{available_categories[category_id]}'
        category_file = os.path.join(basedir, category_file)
        with open(category_file) as json_category:
            questions = json.load(json_category)
            return questions


def getEntityCategories(entity_id, locale="en"):
    url = 'https://query.wikidata.org/sparql'
    query = """
            SELECT
              ?category ?categoryLabel
            WHERE {
              wd:%s (wdt:P31|wdt:P279)* ?category.

              SERVICE wikibase:label { bd:serviceParam wikibase:language "%s". }
            }
        """ % (entity_id, locale)
    r = requests.get(url, params={'format': 'json', 'query': query})
    data = r.json()
    results = data['results']['bindings'][:9]
    # normalizeIDs = lambda x: {"id": x['category']['value'].split('/')[-1], "label": x['categoryLabel']['value']}
    normalizeIDs = lambda x: x['category']['value'].split('/')[-1]
    identifiers = map(normalizeIDs, results)
    # idList = list(identifiers)
    idSet = set(identifiers)
    return idSet


def isValidCategory(category_id):
    if category_id == 'Q52511956':
        return True
    return False
