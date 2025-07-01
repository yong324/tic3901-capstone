import os
from datetime import timedelta

class BaseConfig:
    SECRET_KEY           = os.getenv("SECRET_KEY", "change-me-dev")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///local.db")

    # JWT — Flask-JWT-Extended settings
    JWT_SECRET_KEY       = os.getenv("JWT_SECRET_KEY", "change-me-dev")
    JWT_TOKEN_LOCATION   = ["cookies"]
    JWT_COOKIE_SECURE    = True                    # HTTPS only in prod
    JWT_COOKIE_SAMESITE  = "Lax"
    JWT_ACCESS_TOKEN_EXPIRES  = timedelta(minutes=5)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

class DevConfig(BaseConfig):
    DEBUG = True
    JWT_COOKIE_SECURE = False                   

class TestConfig(BaseConfig):
    TESTING = True
    JWT_COOKIE_SECURE = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

class ProdConfig(BaseConfig):
    DEBUG = False
