from wikidata.client import Client
from themeSelector import ThemeSelector

# Making the search
selector = ThemeSelector()
keys = selector.getKeys('Madrid')

for key in keys:
    print(key)

selectedKey = keys[0]

if(selectedKey is not None):
    # Getting the entity
    client = Client()  # doctest: +SKIP
    entity = client.get(selectedKey["id"], load=True)
    print('Selected entity info: ')
    print(entity)
