import pytest

from endpoints import routes
from main import app as flask_app


@pytest.fixture(autouse=True)
def reset_storage():
    routes.reset_storage()
    yield
    routes.reset_storage()


@pytest.fixture
def client():
    flask_app.config.update(TESTING=True)
    with flask_app.test_client() as client:
        yield client
