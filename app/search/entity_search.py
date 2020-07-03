from app.wikidata import wikidata_service as Wikidata


def get_language(lang):
    """
        Checks that the language entered by the user is a supported language.
        If not valid, it defaults to English.
    """
    if lang in ['es', 'pt', 'fr', 'it']:
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
