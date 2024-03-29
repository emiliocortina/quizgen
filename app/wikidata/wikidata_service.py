import time

import requests

from app.exceptions.invalid_usage import InvalidUsage
from app.wikidata.queries import label_query, correct_answer_query, distractors_query, additional_info_query


def get_entity_label(entity_id, locale):
    """
    Function that returns the label associated to a given Wikidata entity.
    :param entity_id: Wikidata identifier for the entity.
    :param locale: language used to retrieve the label.
    :return: String representing the entity as a label.
    """
    query = label_query % (entity_id, locale)
    labels = make_query(query)
    return labels[0]['label']['value']


def get_correct_answer(entity_id, property_id, lang='en'):
    """
    Obtains the entity that is the object in the statement: entity_id property_id object.
    This entity is the correct answer to the question.
    :param entity_id: subject of the statement.
    :param property_id: predicate of the statement.
    :param lang: language used to retrieve the information
    :return: object in the statement: entity_id property_id object.
    """
    query = correct_answer_query.format(entity=entity_id, property=property_id, language=lang)
    entities = make_query(query)
    entity = entities[0]
    add_additional_info(entity)
    return entity


def get_distractors(entity_id, property_id, lang='en'):
    """
    Obtains distractor entities, that is, entities that appear as objects in statements of the form:
    subject property_id object; where subject!=entity_id (They would be correct answers).
    :param entity_id: Entity we are generating the questions about
        (the subject of the statement for correct answers).
    :param property_id: predicate of the statement.
    :param lang: language used to retrieve the information
    :return: object in the statement: subject property_id object.
    """
    entities_query = distractors_query.format(property=property_id, entity=entity_id, language=lang)
    entities = make_query(entities_query)
    for entity in entities:
        add_additional_info(entity)
    return entities


def add_additional_info(entity):
    """
    Adds additional data to an entity object that represents an answer.
    :param entity: answer entity with additional information.
    """
    entity_id = entity['entity']['value'].split('/')[-1]
    additional_info = get_entity_additional_info(entity_id)
    entity['additionalInfo'] = additional_info


def get_entity_additional_info(entity_id):
    query = additional_info_query % (entity_id, entity_id)
    additional_info = make_query(query)
    if (len(additional_info) > 0):
        return additional_info[0]
    else:
        return {}


def make_query(query):
    """
    Sends an http request to Wikidata's query service with a SPARQL query.
    :param query: String representing a SPARQL query.
    :return: results retrieved from wikidata, error otherwise.
    """
    url = 'https://query.wikidata.org/sparql'
    r = requests.get(url, params={'format': 'json', 'query': query}, timeout=60)
    while r.status_code == 429:
        time.sleep(1.2)
        r = requests.get(url, params={'format': 'json', 'query': query})
    if r.status_code != 200:
        raise IndexError()
    data = r.json()
    return data['results']['bindings']


def search_wd_entities(label, language):
    """
    Uses Wikidata's API to obtain the entities related to a given label.
    :param label: string used to search similar entities.
    :return: array of results obtained (each result contains id and description).
    """
    r = requests.get(
        f'https://www.wikidata.org/w/api.php?action=wbsearchentities&search={label}&language={language}'
        f'&uselang={language}&format=json')
    r = r.json()
    objects = r["search"]
    length = 10 if len(r["search"]) > 10 else len(r["search"])
    keys = []
    for i in range(0, length):
        keys.append(objects[i])
    if len(keys) == 0:
        raise InvalidUsage('No entities found for given label.', status_code=404)
    return keys

