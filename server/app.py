from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from server.models import db, Message

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    CORS(app)
    db.init_app(app)
    migrate = Migrate(app, db)

    @app.route('/messages', methods=['GET'])
    def get_messages():
        messages = Message.query.order_by(Message.created_at.asc()).all()
        return jsonify([message.to_dict() for message in messages])

    @app.route('/messages', methods=['POST'])
    def create_message():
        data = request.get_json()
        message = Message(body=data['body'], username=data['username'])
        db.session.add(message)
        db.session.commit()
        return jsonify(message.to_dict()), 201

    @app.route('/messages/<int:id>', methods=['PATCH'])
    def update_message(id):
        message = Message.query.get_or_404(id)
        data = request.get_json()
        message.body = data['body']
        db.session.commit()
        return jsonify(message.to_dict())

    @app.route('/messages/<int:id>', methods=['DELETE'])
    def delete_message(id):
        message = Message.query.get_or_404(id)
        db.session.delete(message)
        db.session.commit()
        return jsonify({'success': True}), 200

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(port=5555, debug=True)
