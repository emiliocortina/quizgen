from src.wikidata import wikidata_service as Wikidata


def search_entities(label):
    """
    Obtains entities related to a given label.
    :param label: string used to search similar entities.
    :return: array of results obtained (each result contains id and description).
    """
    keys = Wikidata.search_wd_entities(label)
    return keys
