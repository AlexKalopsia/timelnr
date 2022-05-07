from flask import Flask
from sqlalchemy import create_engine
from timelnr.config import Config

app = Flask(__name__)
config = Config()

app.config.from_object(config)
app.secret_key = config.SECRET_KEY

db = create_engine(config.SQLALCHEMY_DATABASE_URI,
                   pool_pre_ping=True, pool_recycle=3600)


# Imported here to avoid circular import
from timelnr import routes
