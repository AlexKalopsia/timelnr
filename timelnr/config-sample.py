# INSERT YOUR DATA AND RENAME THIS FILE TO config.py 

from timelnr.models import Label

class Config:
    DB_HOST = 'YOUR_DATABASE_HOST' # EXAMPLE: http://192.168.0.50:3306 
    DB_USER = 'YOUR_DATABASE_USER'
    DB_PSW = 'YOUR_DATABASE_PASSWORD'
    DB_NAME = 'YOUR_DATABASE_NAME'
    DB_TABLE_PREFIX = 'YOUR_TABLE PREFIX' # EXAMPLE 'mgt_'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}/{}'.format(
        DB_USER, DB_PSW, DB_HOST, DB_NAME)
    SPREADSHEET_ID = 'YOUR_GOOGLESHEET_ID'
    SPREADSHEET_ENTRIES_RANGE = 'YOUR_ENTRIES_RANGE'    # EXAMPLE 'Entries!A3:V234'
    SPREADSHEET_LABELS_RANGE = 'YOUR_LABELS_RANGE'      # EXAMPLE 'Labels!A3:D12'
    SPREADSHEET_LANG_RANGE = 'YOUR_LANGUAGES_RANGE'     # EXAMPLE 'Languages!A1:C15'


# Unused languages should be removed
langs = {
    'en': 'English',
    'it': 'Italiano',
    'fr': 'Français',
    'de': 'Deutsch',
    'es': 'Español',
    'nl': 'Nederlands',
    'lb': 'Lëtzebuergesch',
    'da': 'Danish',
    'br': 'Português brasileiro',
    'pl': 'Polski',
    'uk': 'Ukranian',
    'ru': 'Ру́сский язы́к',
    'ch': '正體中文',
    'fa': 'فارسی',
    'ar': 'اَلْعَرَبِيَّةُ‎'}