import json
import time
import requests
from requests.exceptions import ReadTimeout
from categories.manager import getEntityCategory, getCategoryQuestions, isValidCategory


def generateQuestions(entity_id, n_questions=5, questions_category='Q52511956', locale="en"):
    yield '{"questions": ['
    start_time = time.time()
    if not isValidCategory(questions_category):
        return '\'Please enter a valid category\''
    else:
        templates = getCategoryQuestions(questions_category, locale)
        if len(templates) > 0:
            prev_element = next(templates.__iter__())
            q = generateQuestion(entity_id, prev_element, templates[prev_element], locale)
            if q is not None:
                yield json.dumps(q)
            for property_id in templates:
                q = generateQuestion(entity_id, property_id, templates[property_id], locale)
                if q is not None:
                    yield ','
                    yield json.dumps(q)
        elapsed_time = time.time() - start_time
        print('********** ELAPSED:  ELAPSED: ', elapsed_time, '**********')
    yield ']}'
    return ''


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
    SELECT DISTINCT ?distractorEntity ?distractorEntityLabel ?distractorEntityDescription
    WHERE {
      ?subject wdt:%s ?distractorEntity.
      FILTER NOT EXISTS {
        wd:%s wdt:%s ?distractorEntity.
      }
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    }
    LIMIT 3
    """ % (property_id, entity_id, property_id)

    additional_info_query = """
    SELECT ?distractorEntityType ?distractorEntityImage
    WHERE {
      wd:%s wdt:P31 ?distractorEntityType.
      wd:%s wdt:P18 ?distractorEntityImage.
    }
    LIMIT 5
    """
    entities = makeQuery(entitiesQuery)

    for entity in entities:
        distractor_id = entity['distractorEntity']['value'].split('/')[-1]
        query = additional_info_query % (distractor_id, distractor_id)
        additional_info = makeQuery(query)
        entity['distractorAdditionalInfo'] = additional_info

    return entities


def makeQuery(query):
    url = 'https://query.wikidata.org/sparql'
    r = requests.get(url, params={'format': 'json', 'query': query}, timeout=40)
    while r.status_code == 429:
        time.sleep(1.2)
        r = requests.get(url, params={'format': 'json', 'query': query})
    if r.status_code != 200:
        raise IndexError()
    data = r.json()
    return data['results']['bindings']
