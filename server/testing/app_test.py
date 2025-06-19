import pytest
from server.app import create_app
from server.models import db, Message

@pytest.fixture
def app():
    app = create_app()
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_returns_list_of_json_objects_for_all_messages_in_database(client):
    message = Message(body="Hi", username="Tester")
    db.session.add(message)
    db.session.commit()

    response = client.get('/messages')
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert any(m['body'] == "Hi" for m in response.json)

def test_creates_new_message_in_database(client):
    response = client.post('/messages', json={"body": "Hello 👋", "username": "Liza"})
    assert response.status_code == 201
    assert response.json["body"] == "Hello 👋"
