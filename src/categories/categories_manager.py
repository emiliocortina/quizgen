import os
import json

from src.exceptions.invalid_usage import InvalidUsage


def get_category_questions(category_id):
    """
    Returns the questions associated to a given category.
    :param category_id: identifier representing the category.
    :return: template of questions associated to the given category.
    """
    if category_id is None:
        raise InvalidUsage('Please enter a valid category', status_code=404)
    # Opens the _index.json file that associates each category identifier to a template file
    basedir = os.path.abspath(os.path.dirname(__file__))
    data_file = os.path.join(basedir, 'templates/_index.json')
    with open(data_file) as json_categories:
        available_categories = json.load(json_categories)
        # Check if the requested category doesn't exist in the index
        if not available_categories[category_id]:
            raise InvalidUsage('Please enter a valid category', status_code=404)
        category_file = f'templates/{available_categories[category_id]}'
        category_file = os.path.join(basedir, category_file)
        # Opens the template file containing the questions related to the requested category.
        with open(category_file) as json_category:
            questions = json.load(json_category)
            return questions
