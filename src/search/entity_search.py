from src.wikidata import wikidata_service as Wikidata


def get_language(lang):
    if lang == 'es':
        return lang
    else:
        return 'en'


def search_entities(label, lang):
    """
    Obtains entities related to a given label.
    :param label: string used to search similar entities.
    :return: array of results obtained (each result contains id and description).
    """
    language = get_language(lang)
    keys = Wikidata.search_wd_entities(label, language)
    return keys
