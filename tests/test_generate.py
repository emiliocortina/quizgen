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


def test_valid_generation(client):
    rv = get_generation(client, 'Q312', 'Q18608993', '2', 'es')
    assert rv.status_code == 200
    assert len(rv.json) <= 2

    rv = get_generation(client, 'Q312', 'Q18608993', '0', 'en')
    assert rv.status_code == 200
    assert len(rv.json) == 0


def test_invalid_entity(client):
    rv = get_generation(client, '', 'Q18608993', '2', 'fr')
    assert rv.status_code == 200
    assert len(rv.json) == 0

    rv = get_generation(client, 'Hola', 'Q18608993', '2', 'it')
    assert rv.status_code == 200
    assert len(rv.json) == 0


def test_invalid_template(client):
    rv = get_generation(client, 'Q312', 'Hola', '2', 'pt')
    assert rv.status_code == 404

    rv = get_generation(client, 'Q312', '', '2', 'es')
    assert rv.status_code == 404


def test_invalid_limit(client):
    rv = get_generation(client, 'Q312', 'Q18608993', 'Hola', 'es')
    assert rv.status_code == 200

    rv = get_generation(client, 'Q312', 'Q18608993', '-1', 'es')
    assert rv.status_code == 200


def test_invalid_language(client):
    rv = get_generation(client, 'Q312', 'Q18608993', '2', '')
    assert rv.status_code == 200

    rv = get_generation(client, 'Q312', 'Q18608993', '0', 'ddaskq')
    assert rv.status_code == 200


def get_generation(client, entity, template, limit, language):
    rv = client.get(f'/generate/questions.json?entity={entity}&category={template}&limit={limit}&lang={language}')
    return rv
