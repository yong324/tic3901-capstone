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
    client_name = db.Column(db.String(150), nullable=False)
    permissions = db.Column(db.String(255))  
    added_datetime = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    email = db.Column(db.String(255), nullable=False)

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

if __name__ == '__main__':
    app.run(debug=True)

