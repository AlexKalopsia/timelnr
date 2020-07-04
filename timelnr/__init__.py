from flask import Flask
from sqlalchemy import create_engine
from timelnr.config import Config

app = Flask(__name__)
config = Config()

app.config.from_object(config)

db = create_engine(config.SQLALCHEMY_DATABASE_URI)


# Imported here to avoid circular import
from timelnr import routes
