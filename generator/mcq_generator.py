import requests


def generateQuestions(entity_id, n_questions=5, locale="en"):
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
    normalizeIDs = lambda x: {"id": x['category']['value'].split('/')[-1], "label": x['categoryLabel']['value']}
    identifiers = map(normalizeIDs, results)
    idList = list(identifiers)
    return {"categories": idList}
