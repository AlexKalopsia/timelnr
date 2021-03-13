from __future__ import print_function
import pickle
import os.path
from timelnr import db, config

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from sqlalchemy import Column, Integer, MetaData, String, Table

# Importer.py fetches the timeline multilanguage data from 
# an external google sheet, and stores the data in a MySQL database

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

def getSpreadsheets():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        print('Loading credentials from file...')
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print('Refreshing access token...')
            creds.refresh(Request())
        else:
            print('Fetching new tokens...')
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            print('Saving credentials for future use...')
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    return service.spreadsheets()


def getValuesFromSheet(spreadsheets, _range):
    result = spreadsheets.values().get(spreadsheetId=config.SPREADSHEET_ID,
                                range=_range).execute()
    values = result.get('values', [])
    return values

sheet = getSpreadsheets()
metadata = MetaData()

langs = {}

def createTable(tableType):

    metadata.clear()

    with db.connect() as connection:
        print('Wiping existing '+tableType+' table...')
        connection.execute('DROP TABLE IF EXISTS `' + config.DB_TABLE_PREFIX + tableType+'`')

    print('Preparing '+tableType+' table...')
    table = None
    values = None

    if tableType == 'languages':
        table = Table(config.DB_TABLE_PREFIX + 'languages', metadata,
                     Column('ID', Integer, primary_key=True),
                     Column('Slug', String(20)),
                     Column('Name', String(30)),
                     mysql_charset='utf8mb4'
                     )
        values = getValuesFromSheet(sheet, config.SPREADSHEET_LANG_RANGE)
        for value in values:
            langs[value[1]] = value[2]

    elif tableType == 'entries':
        table = Table(config.DB_TABLE_PREFIX + 'entries', metadata,
                     Column('ID', Integer, primary_key=True),
                     Column('Year', String(4)),
                     Column('Game', String(7)),
                     Column('Color', String(9)),
                     Column('Source', String(4)),
                     Column('Image', String(50)),
                     Column('Video', String(10)),
                     mysql_charset='utf8mb4'
                     )
        for lang in langs:
            table.append_column(Column('Event_' + lang, String(900)))
        values = getValuesFromSheet(sheet, config.SPREADSHEET_ENTRIES_RANGE)
    elif tableType == 'labels':
        table = Table(config.DB_TABLE_PREFIX + 'labels', metadata,
                     Column('ID', Integer, primary_key=True),
                     Column('Slug', String(30)),
                     Column('Name', String(30)),
                     Column('Color', String(7)),
                     mysql_charset='utf8mb4'
                     )
        values = getValuesFromSheet(sheet, config.SPREADSHEET_LABELS_RANGE)
    else:
        table = None
        values = None

    metadata.create_all(db)

    with db.connect() as connection:
        for value in values:
            connection.execute(table.insert().values(value))   
        print('Table '+tableType+' populated correctly')


def main():
    createTable('languages')
    createTable('labels')
    createTable('entries')
    print('Import successful')


if __name__ == '__main__':
    main()