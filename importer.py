from __future__ import print_function
import os.path
from timelnr import db, config
import gspread

from sqlalchemy import Column, Integer, MetaData, String, Table

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# Importer.py fetches the timeline multilanguage data from 
# an external google sheet, and stores the data in a MySQL database


def getSpreadsheets():
    sa = gspread.service_account(filename="service_account.json")
    sh = sa.open_by_key(config.SPREADSHEET_ID)
    return sh


def getValuesFromSheet(spreadsheets, _range):

    ws_name = _range.split("!")[0]
    ws_range = _range.split("!")[1]

    ws = spreadsheets.worksheet(ws_name)
    result = ws.get(ws_range)
    return result

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
        print('Table ' + config.DB_TABLE_PREFIX + tableType + ' populated correctly\n')


def main():
    print('Timelnr Importer\n---------------\n')
    createTable('languages')
    createTable('labels')
    createTable('entries')
    print('Import successful!')


if __name__ == '__main__':
    main()