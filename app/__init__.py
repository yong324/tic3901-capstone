import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

db = SQLAlchemy()
jwt = JWTManager()

def create_app(test_config=None):
    load_dotenv()
    app = Flask(__name__)
    CORS(app, supports_credentials=True)

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

        app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'dev-secret-change-me')
        app.config['JWT_TOKEN_LOCATION'] = ['cookies']
        app.config['JWT_COOKIE_SECURE'] = not app.debug  # True in production only
        app.config['JWT_COOKIE_SAMESITE'] = 'Lax'
        app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 600      # 10 min
        app.config['JWT_REFRESH_TOKEN_EXPIRES'] = 2592000 # 30 days

    db.init_app(app)
    jwt.init_app(app)

    from app.routes import register_routes
    register_routes(app)

    return app

app = create_app()
