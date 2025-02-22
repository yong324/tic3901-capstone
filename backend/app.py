import random
import string
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes and origins

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:tic3901?!@database-1.ct422ga2wer2.ap-southeast-1.rds.amazonaws.com:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# User model
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

# API route for login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Fetch user from the database
    user = UserCredentials.query.filter_by(username=username, password=password).first()
    if user:
        return jsonify({"message": "Login successful", "role": user.role, "user_id": user.user_id}), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401

# API route for retrieving all client metadata
@app.route('/client_metadata', methods=['GET'])
def get_client_metadata():
    try:
        clients = ClientMetadata.query.all()
        clients_list = [
            {
                "client_id": client.client_id,
                "client_name": client.client_name,
                "permissions": client.permissions,
                "added_datetime": client.added_datetime.isoformat() if client.added_datetime else None,
                "email": client.email
            }
            for client in clients
        ]
        return jsonify(clients_list), 200
    except Exception as e:
        return jsonify({"message": "Failed to fetch client metadata", "error": str(e)}), 500

# Utility function to generate password with client name like "client1_xxxx"
def generate_password(client_name):
    # Generate 4 random alphanumeric characters
    rand_chars = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
    return f"{client_name}_{rand_chars}"

# API route for adding new client data
@app.route('/client', methods=['POST'])
def add_client():
    data = request.get_json()
    client_name = data.get('clientName')
    client_email = data.get('clientEmail')
    sftp_username = data.get('sftpUserName')

    if not client_name or not client_email or not sftp_username:
        return jsonify({"message": "Client Name, Client Email and SFTP Username are required."}), 400
    
    # Check if a client with the same name already exists
    existing_client = ClientMetadata.query.filter_by(client_name=client_name).first()
    if existing_client:
        return jsonify({"message": "Client name must be unique. This client name already exists."}), 400

    try:
        # Create a new client in client_metadata table
        new_client = ClientMetadata(
            client_name=client_name,
            email=client_email,
            permissions=''  # set a default permissions value if needed
        )
        db.session.add(new_client)
        db.session.flush()  # flush to assign new_client.client_id without committing

        # Create related record in client_sftp_metadata table
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
            "client": {
                "client_id": new_client.client_id,
                "client_name": new_client.client_name,
                "email": new_client.email,
                "sftp_username": new_sftp.sftp_username,
                "sftp_directory": new_sftp.sftp_directory,
                "password": new_sftp.password
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Failed to add client", "error": str(e)}), 500


from sqlalchemy.exc import IntegrityError

@app.route('/client/<int:client_id>', methods=['PUT'])
def update_client(client_id):
    data = request.get_json()
    
    # Retrieve the client metadata record
    client = ClientMetadata.query.get(client_id)
    if not client:
        return jsonify({"message": "Client not found"}), 404

    # Update client_metadata fields if they are provided in the request
    if 'client_name' in data:
        client.client_name = data['client_name']
    if 'email' in data:
        client.email = data['email']
    if 'permissions' in data:
        client.permissions = data['permissions']
    
    # Optionally, update the related sftp metadata.
    sftp = ClientSftpMetadata.query.filter_by(client_id=client_id).first()
    if sftp and 'client_name' in data:
        sftp.sftp_directory = data['client_name']
        if 'sftp_username' in data:
            sftp.sftp_username = data['sftp_username']
    
    try:
        db.session.commit()
        return jsonify({
            "message": "Client updated successfully",
            "client": {
                "client_id": client.client_id,
                "client_name": client.client_name,
                "email": client.email,
                "permissions": client.permissions,
                "added_datetime": client.added_datetime.isoformat() if client.added_datetime else None,
            }
        }), 200
    except IntegrityError as ie:
        db.session.rollback()
        # If the error is due to the unique constraint on client_name, show a clear message.
        return jsonify({
            "message": "Failed to update client",
            "error": "Client name must be unique. This client name already exists."
        }), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Failed to update client", "error": str(e)}), 500
    
@app.route('/client/<int:client_id>', methods=['DELETE'])
def delete_client(client_id):
    # Retrieve the client record from client_metadata
    client = ClientMetadata.query.get(client_id)
    if not client:
        return jsonify({"message": "Client not found"}), 404

    # Optionally, delete the associated SFTP metadata record
    sftp_record = ClientSftpMetadata.query.filter_by(client_id=client_id).first()
    if sftp_record:
        db.session.delete(sftp_record)
    
    # Delete the client metadata record
    db.session.delete(client)

    try:
        db.session.commit()
        return jsonify({"message": "Client deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Failed to delete client", "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

