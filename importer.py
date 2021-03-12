from __future__ import print_function
import pickle
import os.path
from timelnr import db, config
from timelnr.config import langs

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from sqlalchemy import Column, Integer, MetaData, String, Table

# Importer.py fetches the timeline multilanguage data from 
# an external google sheet, and stores the data in a MySQL database

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

def getDataFromSheet():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()

    result = sheet.values().get(spreadsheetId=config.SPREADSHEET_ID,
                                range=config.SPREADSHEET_RANGE).execute()
    values = result.get('values', [])
    return values


metadata = MetaData()


def createTable():
    """Create the database table by dynamically looking 
    at the langs defined in the timelnr config file"""

    metadata.clear()

    # Wipe table
    with db.connect() as connection:
        connection.execute('DROP TABLE IF EXISTS `' + config.DB_TABLE + '`')

    # Prepare table
    timeline = Table(config.DB_TABLE, metadata,
                     Column('mgtID', Integer, primary_key=True),
                     Column('mgtYear', String(4)),
                     Column('mgtGame', String(7)),
                     Column('mgtColor', String(9)),
                     Column('mgtSource', String(4)),
                     Column('mgtImg', String(50)),
                     Column('mgtVid', String(10)),
                     mysql_charset='utf8mb4'
                     )
    for lang in langs:
        timeline.append_column(Column('mgtEvent_' + lang, String(900)))
    metadata.create_all(db)
    return timeline

def populateTable(timeline):
    """Add all data to the timeline db"""

    values = getDataFromSheet()
    langCodes = values[1][7:]
    with db.connect() as connection:
        for value in values[2:]:
            connection.execute(timeline.insert().values(value))


def main():
    tl = createTable()
    populateTable(tl)


if __name__ == '__main__':
    main()
