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
        distractors = getDistractors(property_id)
        for distractor in distractors:
            print(distractor['distractorLabel']['value'])
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
      ?answerEntity ?answerType ?answerEntityLabel
    WHERE {
       wd:%s wdt:%s ?answerEntity.
       OPTIONAL {?answerEntity wdt:P31 ?answerType.}

      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    }
    """ % (entity_id, property_id)
    results = makeQuery(query)
    return results[0]


def getDistractors(property_id):
    query = """
    SELECT DISTINCT ?distractorEntity ?distractorType ?distractorLabel
    WHERE {
      ?subject wdt:%s ?distractorEntity.
      OPTIONAL {?distractorLabel wdt:P31 ?distractorType.}

      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    }
    LIMIT 3
    """ % (property_id)
    results = makeQuery(query)
    return results


def makeQuery(query):
    url = 'https://query.wikidata.org/sparql'
    r = requests.get(url, params={'format': 'json', 'query': query}, timeout=20)
    while r.status_code == 429:
        time.sleep(1.2)
        r = requests.get(url, params={'format': 'json', 'query': query})
    if r.status_code != 200:
        print('Error')
    data = r.json()
    return data['results']['bindings']