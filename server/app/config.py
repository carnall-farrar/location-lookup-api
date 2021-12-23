import os


class BaseConfig:
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "my_precious"
    BCRYPT_LOG_ROUNDS = 13
    ACCESS_TOKEN_EXPIRATION = 900
    REFRESH_TOKEN_EXPIRATION = 2592000


class DevelopmentConfig(BaseConfig):
    postgres_user = os.environ.get("POSTGRES_USER")
    postgres_password = os.environ.get("POSTGRES_PASSWORD")
    postgres_host = os.environ.get("POSTGRES_HOST")
    SQLALCHEMY_DATABASE_URI = f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}/location_dev"
    BCRYPT_LOG_ROUNDS = 4


class TestingConfig(BaseConfig):
    TESTING = True
    postgres_user = os.environ.get("POSTGRES_USER")
    postgres_password = os.environ.get("POSTGRES_PASSWORD")
    postgres_host = os.environ.get("POSTGRES_HOST")
    SQLALCHEMY_DATABASE_URI = f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}/location_test"
    BCRYPT_LOG_ROUNDS = 4
    ACCESS_TOKEN_EXPIRATION = 3
    REFRESH_TOKEN_EXPIRATION = 3


class ProductionConfig(BaseConfig):
    postgres_user = os.environ.get("POSTGRES_USER")
    postgres_password = os.environ.get("POSTGRES_PASSWORD")
    postgres_host = os.environ.get("POSTGRES_HOST")
    SQLALCHEMY_DATABASE_URI = f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}/location_dev"
    SECRET_KEY = os.getenv("SECRET_KEY", "my_precious")
