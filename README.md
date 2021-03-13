# Timelnr

Timelnr is a web app built in Pyton, Flesk and Jinja. It was originally built for the [Metal Gear Timeline](https://www.metalgeartimeline.com). All the data from the timeline, as well as some styling information, are pulled from a Google Sheet and stored in an SQL database.

## Requirements

- A MySQL database where the data will be stored
- A Docker environment

## Deployment

1. Setup a MySQL database, and set the credentials in 'timelnr/config.py' as explained in the seciton below
2. Edit `start.sh` to configure your Docker environment (container name, and container port)`
3. Run `start.sh` to build the Docker image and let it run on your server

## Config.py

Open 'timelnr/config.py' to configure Timelnr:

|                           | Description                                                | Example                            |
| ------------------------- | ---------------------------------------------------------- | ---------------------------------- |
| DB_HOST                   | Your database host address                                 | `http://localhost:3306`            |
| DB_USER                   | Your database username                                     | myUser                             |
| DB_PSW                    | Your database password                                     | myPassword                         |
| DB_TABLE_PREFIX           | The table prefix to be used. Should end with an underscore | tln\_                              |
| SPREADSHEET_ID            | The ID of the Google sheet. Can be found in the URL bar    | 1jfdwjDSe_djhJDGDHgfdsjgsdfhj_d3X0 |
| SPREADSHEET_ENTRIES_RANGE | Range covering the timeline entries information            | Entries!A3:V234                    |
| SPREADSHEET_LABELS_RANGE  | Range covering the entry labels                            | Labels!A3:D13                      |
| SPREADSHEET_LANG_RANGE    | Range covering the supported languages                     | Languages!A1:C15                   |

## Sheet structure

In the sheet there should be three pages: Entries (the content of the timeline), Languages (list of supported languages) and Labels (management and styling).

> **_IMPORTANT:_** The sheet structure can be changed, as long as the data ranges defined in `timelnr/config.py` are correct.

The Entries page normally has the following structure:

|     |      |      |       |        |                |     | ENGLISH            | ITALIAN        | ... |
| --- | ---- | ---- | ----- | ------ | -------------- | --- | ------------------ | -------------- | --- |
| ID  | YEAR | GAME | COLOR | SOURCE | IMG            | VID | en                 | it             | ... |
| 1   | 2001 | MGS2 | mgs2  |        | mgs2header.jpg |     | Snake is born      | Nasce Snake    | ... |
| 2   |      |      |       |        |                |     | Everyone loves him | Tutti lo amano | ... |
| 3   | 2012 | MGS4 | mgs4  |        | mgs4.png       |     | Snake is dead      | Muore Snake    | ... |
| ... | ...  | ...  | ...   | ...    | ...            | ... | ...                | ...            | ... |

- **ID**: entry ID. Must be unique
- **YEAR**: the year when a specific timeline entry happened
- **GAME**: title of the game. Should be used only for the first entry belonging to the game
- **COLOR**: css class defined in 'timelnr/config.py'
- **SOURCE**: unused. Refers to the game that is source of that information
- **IMG**: name of the image relative to the entry. Stored in `timelnr/static/images/`
- **VID**: unused. link to a YouTube video related to the entry

> **_IMPORTANT:_** The first entry under every language column needs to be the relative language code (refer to [this list](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes)), which should also match the one defined in the Languages page.

## How to

### Pull the data from the Google Sheet

1. Go on the [Google Developer Console](https://console.developers.google.com)
2. Create a project and generate a OAuth 2.0 Client ID
3. Download the credentials as JSON file
4. Store the JSON file in the project root
5. Simply run `py importer.py`

> **_NOTE:_** `importer.py` pulls data from the translation sheet via the Google API. To do this it relies on the dev credentials stored in `credentials.json` (which is not included in the repo). The file can be re-downloaded from your developer console.

### Update the timeline entries

1. Edit the entries inside the Google Sheet
2. Run `py importer.py` to rebuild the database

### Add new languages

1. Make sure that the relative column in the Entries sheet page has the right language code
2. Make sure the Languages sheet page contains the new language. Currently the order needs to match the one in the Sheet.
3. Run `py imorter.py`. This will recreate the SQL database
4. Rebuild docker image with `sh start.sh`

### Change styling and labels

1. Edit the CSS files you want to change
2. Edit the labels colors from the Labels page of the sheet
3. Restart the Docker container with `docker restart mgt`
