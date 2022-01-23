# Automatic generation of multiple-choice questions using knowledge graphs

## Description
See attached PDF file [Automatic generation of multiple choice questions using knowledge graphs.pdf](https://github.com/emiliocortina/quizgen/blob/master/Automatic%20generation%20of%20multiple%20choice%20questions%20using%20knowledge%20graphs.pdf)

## Create a virtual environment
Command line

Navigate into quizgen folder

    cd quizgen

To install dependencies locally instead of globally, in linux/mac run:

    python3 -m venv .venv
    source .venv/bin/activate

## Install dependencies

    pip install -r requirements.txt

## Run 

    export FLASK_APP=app
    flask run

## Test

    python -m pytest

## Links

### Wikidata
* Qwikidata: https://qwikidata.readthedocs.io/en/stable/readme.html
* Docs: https://wikidata.readthedocs.io/en/stable/index.html
* Tools: https://www.wikidata.org/wiki/Wikidata:Tools/For_programmers
* Search by label: https://www.wikidata.org/w/api.php?action=help&modules=wbsearchentities
from https://stackoverflow.com/questions/27452656/wikidata-entity-value-from-name
* Example of search by label: https://www.wikidata.org/w/api.php?action=wbsearchentities&search=Spain&language=en&format=json
* Sparql queries: https://janakiev.com/blog/wikidata-mayors/

### Python tools
* Python Requests (http requests): https://requests.kennethreitz.org/en/master/
* Python imports: https://stackoverflow.com/questions/2349991/how-to-import-other-python-files
* Flask tutorial: https://medium.com/@onejohi/building-a-simple-rest-api-with-python-and-flask-b404371dc699
 https://www.youtube.com/watch?v=PTZiDnuC86g
* Lambda map and filter: https://medium.com/better-programming/lambda-map-and-filter-in-python-4935f248593

### Other links
* Heroku timeout: https://librenepal.com/article/flask-and-heroku-timeout/
* Flask generators: https://blog.al4.co.nz/2016/01/streaming-json-with-flask/


Problemas:
Moncayo continente: Europa (Jupiter)
https://www.wikidata.org/wiki/Q690347 continente california
