import pytest

from app import create_app


@pytest.fixture()
def app():
    app = create_app({ 
        'DB_CONNECTION': 'sqlite://',
        'SECRET_KEY': 'test-key',
        'TESTING': True
    })

    from app.database import create_db      
    create_db()

    yield app


@pytest.fixture()
def client(app):
    yield app.test_client()