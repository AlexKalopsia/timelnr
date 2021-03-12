from timelnr.models import Label


class Config:
    DB_HOST = 'YOUR_DATABASE_HOST'
    DB_USER = 'YOUR_DATABASE_USER'
    DB_PSW = 'YOUR_DATABASE_PASSWORD'
    DB_NAME = 'YOUR_DATABASE_NAME'
    DB_TABLE = 'YOUR_DATABASE_TABLE'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}/{}'.format(
        DB_USER, DB_PSW, DB_HOST, DB_NAME)
    SPREADSHEET_ID = 'YOUR_GOOGLESHEET_ID'
    SPREADSHEET_RANGE = 'YOUR_GOOGLESHEET_RANGE' #EXAMPLE: 'Sheet1!A1:V234'


# REMOVE UNUSED LANGUAGES OR ADD NEW ONES
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

