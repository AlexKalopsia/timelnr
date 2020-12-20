from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from timelnr import db, config
from timelnr.config import langs

from sqlalchemy import Column, Integer, MetaData, String, Table

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1j0TOhkauHv_E3xzWseriABLFGmYSQ0c0kGoNgx_d3Xo'
SAMPLE_RANGE_NAME = 'Sheet1!A1:V234'


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

    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])
    return values


metadata = MetaData()


def createTable():
    """Create the table by dynamically looking at the langs"""
    metadata.clear()

    with db.connect() as connection:
        connection.execute('DROP TABLE IF EXISTS `' + config.DB_TABLE + '`')

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


tl = createTable()


def populateTable():
    """Add all data to the timeline db"""

    values = getDataFromSheet()
    langCodes = values[1][7:]
    with db.connect() as connection:
        for value in values[2:]:
            connection.execute(tl.insert().values(value))


def main():
    createTable()
    populateTable()


if __name__ == '__main__':
    main()
