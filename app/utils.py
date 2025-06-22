from sqlalchemy.exc import IntegrityError
from flask import jsonify
import random
import string
from app.models import ClientMetadata, ClientPermissions
from app import db

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
    permissions = [p.permission for p in ClientPermissions.query.filter_by(client_id=client.client_id).all()]
    return {
        "client_id": client.client_id,
        "client_name": client.client_name,
        "permissions": permissions,
        "added_datetime": client.added_datetime.isoformat() if client.added_datetime else None,
        "email": client.email
    }
