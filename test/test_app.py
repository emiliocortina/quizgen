import tempfile
import pytest

from quizgen import create_app


# This client fixture will be called by each individual test.
# It gives us a simple interface to the application,
# where we can trigger test requests to the application
@pytest.fixture
def client():
    quizgen = create_app()
    quizgen.config['TESTING'] = True

    with quizgen.test_client() as client:
        yield client


def test_server_works(client):
    rv = client.get('/')
    assert b'Server Works!' in rv.data
