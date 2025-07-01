from flask import request, jsonify
from sqlalchemy.exc import IntegrityError
import bcrypt

from app import db
from app.models import (
    UserCredentials, ClientMetadata, ClientPermissions, ClientSftpMetadata
)
from app.utils import (
    generate_password, handle_integrity_error, get_client_by_id, format_client
)

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    create_access_token,
    create_refresh_token,
    set_access_cookies,
    set_refresh_cookies,
    unset_jwt_cookies,
)

def register_routes(app):
    @app.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        print("Login attempt received:")
        print("Username:", username)
        print("Password:", password)

        if not username or not password:
            return jsonify({"message": "Username and password are required"}), 400

        user = UserCredentials.query.filter_by(username=username).first()
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            access_token  = create_access_token(identity=str(user.user_id))   
            refresh_token = create_refresh_token(identity=str(user.user_id))  

            print("JWT tokens generated")
            resp = jsonify({
                "message": "Login successful",
                "role":    user.role,
                "user_id": user.user_id
            })
            set_access_cookies(resp,  access_token)   
            set_refresh_cookies(resp, refresh_token) 
            return resp, 200

        return jsonify({"message": "Invalid username or password"}), 401

    @app.route('/refresh', methods=['POST'])
    @jwt_required(refresh=True)
    def refresh():
        user_id = get_jwt_identity()
        access  = create_access_token(identity=user_id)
        resp    = jsonify({"message": "Token refreshed"})
        set_access_cookies(resp, access)
        return resp, 200

    @app.route('/logout', methods=['POST'])
    def logout():
        resp = jsonify({"message": "Logout successful"})
        unset_jwt_cookies(resp)
        return resp, 200

    @app.route('/register', methods=['POST'])
    def register():
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'message': 'Username and password are required'}), 400

        if len(password) <= 6:
            return jsonify({'message': 'Password must be more than 6 characters.'}), 400

        try:
            hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            new_user  = UserCredentials(username=username, password=hashed_pw, role='user')
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'message': 'User registered successfully'}), 201

        except IntegrityError:
            db.session.rollback()
            return jsonify({'message': 'Username already exists.'}), 409
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': 'Registration failed', 'error': str(e)}), 500


    @app.route('/client_metadata', methods=['GET'])
    @jwt_required()
    def get_client_metadata():
        try:
            clients = ClientMetadata.query.all()
            result  = []
            for client in clients:
                sftp      = ClientSftpMetadata.query.filter_by(client_id=client.client_id).first()
                formatted = format_client(client)
                if sftp:
                    formatted['sftp_username']  = sftp.sftp_username
                    formatted['sftp_directory'] = sftp.sftp_directory
                else:
                    formatted['sftp_username']  = ''
                    formatted['sftp_directory'] = ''
                result.append(formatted)
            return jsonify(result), 200
        except Exception as e:
            return jsonify({"message": "Failed to fetch client metadata", "error": str(e)}), 500


    @app.route('/client', methods=['POST'])
    @jwt_required()
    def add_client():
        data          = request.get_json()
        client_name   = data.get('clientName')
        client_email  = data.get('clientEmail')
        sftp_username = data.get('sftpUserName')
        permissions   = data.get('permissions', [])

        if not all([client_name, client_email, sftp_username]):
            return jsonify({"message": "Client Name, Client Email, and SFTP Username are required."}), 400

        try:
            new_client = ClientMetadata(client_name=client_name, email=client_email)
            db.session.add(new_client)
            db.session.flush()

            for perm in permissions:
                db.session.add(ClientPermissions(client_id=new_client.client_id, permission=perm))

            new_sftp = ClientSftpMetadata(
                client_id      = new_client.client_id,
                sftp_directory = client_name,
                sftp_username  = sftp_username,
                password       = generate_password(client_name)
            )
            db.session.add(new_sftp)
            db.session.commit()

            return jsonify({
                "message": "Client added successfully",
                "client":  format_client(new_client),
                "sftp": {
                    "sftp_username":  new_sftp.sftp_username,
                    "sftp_directory": new_sftp.sftp_directory,
                    "password":       new_sftp.password
                }
            }), 201

        except IntegrityError as e:
            db.session.rollback()
            return handle_integrity_error(e)
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": "Failed to add client", "error": str(e)}), 500


    @app.route('/client/<int:client_id>', methods=['PUT'])
    @jwt_required()
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
            ClientPermissions.query.filter_by(client_id=client.client_id).delete()
            for perm in data['permissions']:
                db.session.add(ClientPermissions(client_id=client.client_id, permission=perm))

        sftp = ClientSftpMetadata.query.filter_by(client_id=client_id).first()
        if sftp:
            if 'sftp_directory' in data:
                sftp.sftp_directory = data['sftp_directory']
            if 'sftp_username' in data:
                sftp.sftp_username = data['sftp_username']

        try:
            db.session.commit()
            return jsonify({
                "message": "Client updated successfully",
                "client":  format_client(client),
                "sftp": {
                    "sftp_username":  sftp.sftp_username if sftp else None,
                    "sftp_directory": sftp.sftp_directory if sftp else None
                }
            }), 200
        except IntegrityError as e:
            db.session.rollback()
            return handle_integrity_error(e)
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": "Failed to update client", "error": str(e)}), 500


    @app.route('/client/<int:client_id>', methods=['DELETE'])
    @jwt_required()
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
