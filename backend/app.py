# app.py
import random
import string
import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv

db = SQLAlchemy()


def create_app(test_config=None):
    load_dotenv()

    app = Flask(__name__)
    CORS(app)

    if test_config:
        app.config.update(test_config)
    else:
        db_user = os.getenv('DB_USERNAME')
        db_password = os.getenv('DB_PASSWORD')
        db_host = os.getenv('DB_HOST')
        db_port = os.getenv('DB_PORT')
        db_name = os.getenv('DB_NAME')

        app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    register_routes(app)

    return app


# ================================
# Models
# ================================
class UserCredentials(db.Model):
    __tablename__ = 'user_credentials'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), default='user')
    created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())


class ClientMetadata(db.Model):
    __tablename__ = 'client_metadata'
    client_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client_name = db.Column(db.String(150), nullable=False, unique=True)
    permissions = db.Column(db.String(255))
    added_datetime = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    email = db.Column(db.String(255), nullable=False)
    sftp_records = db.relationship('ClientSftpMetadata', backref='client', cascade="all, delete")


class ClientSftpMetadata(db.Model):
    __tablename__ = 'client_sftp_metadata'
    client_id = db.Column(db.Integer, db.ForeignKey('client_metadata.client_id'), primary_key=True)
    sftp_directory = db.Column(db.String(150), nullable=False)
    sftp_username = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(255), nullable=False)


# ================================
# Utility Functions
# ================================
def generate_password(client_name):
    rand_chars = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
    return f"{client_name}_{rand_chars}"


def handle_integrity_error(e):
    if "client_name" in str(e):
        return {"message": "Client name must be unique."}, 400
    return {"message": "Database integrity error", "error": str(e)}, 400


def get_client_by_id(client_id):
    client = db.session.get(ClientMetadata, client_id)
    if not client:
        return None, {"message": "Client not found"}, 404
    return client, None, 200



def format_client(client):
    return {
        "client_id": client.client_id,
        "client_name": client.client_name,
        "permissions": client.permissions,
        "added_datetime": client.added_datetime.isoformat() if client.added_datetime else None,
        "email": client.email
    }


# ================================
# Routes
# ================================
def register_routes(app):
    @app.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        username, password = data.get('username'), data.get('password')
        user = UserCredentials.query.filter_by(username=username, password=password).first()
        if user:
            return jsonify({"message": "Login successful", "role": user.role, "user_id": user.user_id}), 200
        return jsonify({"message": "Invalid username or password"}), 401

    @app.route('/client_metadata', methods=['GET'])
    def get_client_metadata():
        try:
            clients = ClientMetadata.query.all()
            return jsonify([format_client(client) for client in clients]), 200
        except Exception as e:
            return jsonify({"message": "Failed to fetch client metadata", "error": str(e)}), 500

    @app.route('/client', methods=['POST'])
    def add_client():
        data = request.get_json()
        client_name = data.get('clientName')
        client_email = data.get('clientEmail')
        sftp_username = data.get('sftpUserName')

        if not all([client_name, client_email, sftp_username]):
            return jsonify({"message": "Client Name, Client Email, and SFTP Username are required."}), 400

        try:
            new_client = ClientMetadata(client_name=client_name, email=client_email, permissions='')
            db.session.add(new_client)
            db.session.flush()

            new_sftp = ClientSftpMetadata(
                client_id=new_client.client_id,
                sftp_directory=client_name,
                sftp_username=sftp_username,
                password=generate_password(client_name)
            )
            db.session.add(new_sftp)
            db.session.commit()

            return jsonify({
                "message": "Client added successfully",
                "client": format_client(new_client),
                "sftp": {
                    "sftp_username": new_sftp.sftp_username,
                    "sftp_directory": new_sftp.sftp_directory,
                    "password": new_sftp.password
                }
            }), 201

        except IntegrityError as e:
            db.session.rollback()
            return handle_integrity_error(e)
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": "Failed to add client", "error": str(e)}), 500

    @app.route('/client/<int:client_id>', methods=['PUT'])
    def update_client(client_id):
        client, error_response, status_code = get_client_by_id(client_id)
        if error_response:
            return jsonify(error_response), status_code

        data = request.get_json()
        if 'client_name' in data:
            client.client_name = data['client_name']
        if 'email' in data:
            client.email = data['email']
        if 'permissions' in data:
            client.permissions = data['permissions']

        sftp = ClientSftpMetadata.query.filter_by(client_id=client_id).first()
        if sftp and 'client_name' in data:
            sftp.sftp_directory = data['client_name']
            if 'sftp_username' in data:
                sftp.sftp_username = data['sftp_username']

        try:
            db.session.commit()
            return jsonify({"message": "Client updated successfully", "client": format_client(client)}), 200
        except IntegrityError as e:
            db.session.rollback()
            return handle_integrity_error(e)
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": "Failed to update client", "error": str(e)}), 500

    @app.route('/client/<int:client_id>', methods=['DELETE'])
    def delete_client(client_id):
        client, error_response, status_code = get_client_by_id(client_id)
        if error_response:
            return jsonify(error_response), status_code

        try:
            db.session.delete(client)
            db.session.commit()
            return jsonify({"message": "Client deleted successfully"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": "Failed to delete client", "error": str(e)}), 500


# Only used when running locally
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
