import pytest

from app import create_app


# This client fixture will be called by each individual test.
# It gives us a simple interface to the application,
# where we can trigger test requests to the application
@pytest.fixture
def client():
    quizgen = create_app()
    quizgen.config['TESTING'] = True

    with quizgen.test_client() as client:
        yield client


def test_valid_search(client):
    rv = get_search(client, 'Madrid', 'es')
    assert rv.status_code == 200

    rv = get_search(client, 'European Union', 'en')
    assert rv.status_code == 200

    rv = get_search(client, 'Moscú', 'it')
    assert rv.status_code == 200

    rv = get_search(client, 'Madrid', '')
    assert rv.status_code == 200

    rv = get_search(client, 'Madrid', 'portugués')
    assert rv.status_code == 200


def test_invalid_search(client):
    rv = get_search(client, 'aewqkeqw', 'fr')
    assert rv.status_code == 404

    rv = get_search(client, '', 'fr')
    assert rv.status_code == 404


def get_search(client, label, language):
    rv = client.get(f'/search/entities.json?label={label}&lang={language}')
    return rv
