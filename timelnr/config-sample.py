# INSERT YOUR DATA AND RENAME THIS FILE TO config.py

from timelnr.models import Label


class Config:
    SECRET_KEY = b'GENERATE_SECRET_KEY'
    DB_HOST = 'YOUR_DATABASE_HOST'
    DB_USER = 'YOUR_DATABASE_USER'
    DB_PSW = 'YOUR_DATABASE_PASSWORD'
    DB_NAME = 'YOUR_DATABASE_NAME'
    DB_TABLE_PREFIX = 'YOUR_TABLE PREFIX'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}/{}'.format(
        DB_USER, DB_PSW, DB_HOST, DB_NAME)
    SPREADSHEET_ID = 'YOUR_GOOGLESHEET_ID'
    SPREADSHEET_ENTRIES_RANGE = 'YOUR_ENTRIES_RANGE'
    SPREADSHEET_LABELS_RANGE = 'YOUR_LABELS_RANGE'
    SPREADSHEET_LANG_RANGE = 'YOUR_LANGUAGES_RANGE'
