import time
import requests
from requests.exceptions import ReadTimeout
from tfg.categories.manager import getEntityCategory, getCategoryQuestions, isValidCategory


def generateQuestions(entity_id, n_questions=5, questions_category='Q52511956', locale="en"):
    if not isValidCategory(questions_category):
        return ['Please enter a valid category']
    templates = getCategoryQuestions(questions_category, locale)
    questions = []
    for template in templates:
        question = generateQuestion(entity_id, template, templates[template], locale)
        if question is not None:
            questions.append(question)
    return questions


def generateQuestion(entity_id, property_id, statement, locale):
    try:
        print('*' * 10)
        print('Generating question for property: ', property_id)
        entity_label = getEntityLabel(entity_id, locale)
        statement = statement[locale] % entity_label
        print('Statement: ', statement)
        correct_answer = getCorrectAnswer(entity_id, property_id)
        print('Correct Answer: ', correct_answer['answerEntityLabel']['value'])
        distractors = getDistractors(entity_id, property_id)
        for distractor in distractors:
            print(distractor['distractorEntityLabel']['value'])
        return {'statement': statement, 'answer': correct_answer, 'distractors': distractors}
    except IndexError:
        print('Data not found for given property and entity')
    except ReadTimeout:
        print('Time out')
    else:
        print('Some error occurred')
    return None


def getEntityLabel(entity_id, locale):
    query = """
        SELECT DISTINCT * WHERE {
          wd:%s rdfs:label ?label . 
          FILTER (langMatches( lang(?label), "%s" ) )  
        }
        """ % (entity_id, locale)
    labels = makeQuery(query)
    return labels[0]['label']['value']


def getCorrectAnswer(entity_id, property_id):
    query = """
    SELECT
      ?answerEntity (SAMPLE(?type) AS ?answerType) (SAMPLE(?label) AS  ?answerEntityLabel)
    WHERE {
      wd:%s wdt:%s ?answerEntity.
      ?answerEntity rdfs:label ?label . 
      OPTIONAL {?answerEntity wdt:P31 ?type.}
      FILTER (langMatches( lang(?label), "en" ) )
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    }
    GROUP BY ?answerEntity
    """ % (entity_id, property_id)
    results = makeQuery(query)
    return results[0]


def getDistractors(entity_id, property_id):
    entitiesQuery = """
    SELECT DISTINCT ?distractorEntity ?distractorEntityLabel
    WHERE {
        FILTER NOT EXISTS {
            ?distractorEntity wdt:%s wd:%s.
          }
        ?subject wdt:%s ?distractorEntity.

        SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    }
    LIMIT 3
    """ % (property_id, entity_id, property_id)
    typesQuery = """
    SELECT DISTINCT ?distractorEntityType
    WHERE {
      wd:%s wdt:P31 ?distractorEntityType.
    }
    LIMIT 5
    """
    entities = makeQuery(entitiesQuery)

    for entity in entities:
        entity_id = entity['distractorEntity']['value'].split('/')[-1]
        query = typesQuery % entity_id
        types = makeQuery(query)
        entity['distractorEntityTypes'] = types[0]
        pass
    return entities


def makeQuery(query):
    url = 'https://query.wikidata.org/sparql'
    r = requests.get(url, params={'format': 'json', 'query': query}, timeout=60)
    while r.status_code == 429:
        time.sleep(1.2)
        r = requests.get(url, params={'format': 'json', 'query': query})
    if r.status_code != 200:
        raise IndexError()
    data = r.json()
    return data['results']['bindings']
