import random
import string
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes and origins

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:tic3901?!@database-1.ct422ga2wer2.ap-southeast-1.rds.amazonaws.com:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ================================
# Models
# ================================
class UserCredentials(db.Model):
    __tablename__ = 'user_credentials'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # Plain text password
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
    """Generate password with client name like 'client1_xxxx'"""
    rand_chars = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
    return f"{client_name}_{rand_chars}"


def handle_integrity_error(e):
    """Handle integrity errors (e.g., unique constraint violations)"""
    if "client_name" in str(e):
        return {"message": "Client name must be unique."}, 400
    return {"message": "Database integrity error", "error": str(e)}, 400


def get_client_by_id(client_id):
    """Get client by ID or return 404 error"""
    client = ClientMetadata.query.get(client_id)
    if not client:
        return None, {"message": "Client not found"}, 404
    return client, None, 200


def format_client(client):
    """Format client data for JSON response"""
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

# Login Route
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username, password = data.get('username'), data.get('password')

    user = UserCredentials.query.filter_by(username=username, password=password).first()
    if user:
        return jsonify({"message": "Login successful", "role": user.role, "user_id": user.user_id}), 200
    return jsonify({"message": "Invalid username or password"}), 401


# Get All Clients
@app.route('/client_metadata', methods=['GET'])
def get_client_metadata():
    try:
        clients = ClientMetadata.query.all()
        return jsonify([format_client(client) for client in clients]), 200
    except Exception as e:
        return jsonify({"message": "Failed to fetch client metadata", "error": str(e)}), 500


# Add New Client
@app.route('/client', methods=['POST'])
def add_client():
    data = request.get_json()
    client_name, client_email, sftp_username = data.get('clientName'), data.get('clientEmail'), data.get('sftpUserName')

    if not all([client_name, client_email, sftp_username]):
        return jsonify({"message": "Client Name, Client Email, and SFTP Username are required."}), 400

    try:
        # Create new client
        new_client = ClientMetadata(client_name=client_name, email=client_email, permissions='')
        db.session.add(new_client)
        db.session.flush()

        # Create related SFTP metadata
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


# Update Existing Client
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


# Delete Client
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

if __name__ == '__main__':
    app.run(debug=True)
