from src.wikidata import wikidata_service as Wikidata
from requests.exceptions import ReadTimeout
from src.categories.categories_manager import get_category_questions


def generate_questions(entity_id, questions_category, questions_limit=None, locale="en"):
    """
    Main function that generates an array of questions about a given entity.
    :param entity_id: (Wikidata) Identifier for the entity used to generate the questions.
    :param questions_category: (Wikidata) Identifier that represent a group of properties that are related
     between them (category).
    :param questions_limit: maximum number of questions that will be generated
    :param locale: language used to return the questions.
    :return: array of question objects.
    """
    templates = get_category_questions(questions_category)
    questions = []
    limit = get_questions_limit(questions_limit)
    for template in templates:
        q = generate_question(entity_id, template, templates[template], locale)
        if q is not None:
            questions.append(q)
        if len(questions) >= limit:
            break
    return questions


def get_questions_limit(questions_limit):
    try:
        questions_limit = int(questions_limit)
        return questions_limit
    except:
        return float("inf")


def generate_question(entity_id, property_id, statement, locale):
    """
    Function that generates and return a single question given an entity and a property.
    :param entity_id: (Wikidata) Identifier for the entity used to generate the question.
    :param property_id: (Wikidata) Identifier for the property used to generate the question.
    :param statement: String that expresses in natural language the question associated to the property.
    :param locale: language used to return the question.
    :return: question object containing a statement, a correct answer and 3 distractors
    """
    try:
        # Generating question for property_id
        entity_label = get_entity_label(entity_id, locale)
        # Composing the statement with the entity
        statement = statement[locale] % entity_label
        # Obtaining the correct answer
        correct_answer = get_correct_answer(entity_id, property_id)
        # Obtaining the distractors
        distractors = get_distractors(entity_id, property_id)
        # Composing the question object
        question = {'statement': statement, 'correctAnswer': correct_answer, 'distractors': distractors}
        return question
    except IndexError:
        print('Data not found for given property and entity')
    except ReadTimeout:
        print('Time out')
    return None


def get_entity_label(entity_id, locale):
    """
    Returns the label associated to a given (Wikidata) entity.
    :param entity_id: (Wikidata) Identifier representing the entity.
    :param locale: language used to retrieve the label.
    :return: String representing the entity as a label.
    """
    return Wikidata.get_entity_label(entity_id, locale)


def get_correct_answer(entity_id, property_id):
    """
    Returns the correct answer to the question.
    :param entity_id: (Wikidata) Identifier representing the entity.
    :param property_id: (Wikidata) Identifier representing the predicate of the question.
    :return: Answer object representing the correct answer.
    """
    return Wikidata.get_correct_answer(entity_id, property_id)


def get_distractors(entity_id, property_id):
    """
    Returns distractor answers to for the question.
    :param entity_id: (Wikidata) Identifier representing the entity.
    :param property_id: (Wikidata) Identifier representing the predicate of the question.
    :return: Array of answer objects representing the distractor answers.
    """
    return Wikidata.get_distractors(entity_id, property_id)
