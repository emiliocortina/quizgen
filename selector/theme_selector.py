import requests

class EntitySelector:

    def search_entities(self, label):
        r = requests.get(f'https://www.wikidata.org/w/api.php?action=wbsearchentities&search={label}&language=en&format=json')
        r = r.json()
        objects = r["search"]
        length = 10 if len(r["search"]) > 10 else len(r["search"])
        keys = []
        for i in range(0, length):
            keys.append(objects[i])
        return keys
