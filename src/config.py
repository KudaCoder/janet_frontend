import os
from dotenv import load_dotenv

BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR, ".env"))

POSTGRES_HOST = os.environ.get("JANET_POSTGRES_HOST")
POSTGRES_PORT = os.environ.get("JANET_POSTGRES_PORT")
POSTGRES_USER = os.environ.get("JANET_POSTGRES_USER")
POSTGRES_PW = os.environ.get("JANET_POSTGRES_PW")
POSTGRES_DB = os.environ.get("JANET_POSTGRES_DB")
DB_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PW}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "abc"
    SQLALCHEMY_DATABASE_URI = DB_URL or f"psql:///{os.path.join(basedir)}"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
