import pytest
from datetime import datetime
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

def test_message_model_has_correct_columns(app):
    """has columns for message body, username, and creation time"""
    message = Message(body="Hello 👋", username="Liza")
    db.session.add(message)
    db.session.commit()

    assert message.id is not None
    assert message.body == "Hello 👋"
    assert message.username == "Liza"
    assert isinstance(message.created_at, datetime)

def test_message_model_to_dict(app):
    """returns dictionary representation of the message"""
    message = Message(body="Testing", username="TestUser")
    db.session.add(message)
    db.session.commit()

    message_dict = message.to_dict()
    assert isinstance(message_dict, dict)
    assert message_dict['body'] == "Testing"
    assert message_dict['username'] == "TestUser"
