# Timelnr

Timelnr is a web app built in Pyton, Flask and Jinja. It was originally built for the [Metal Gear Timeline](https://www.metalgeartimeline.com). All the data from the timeline, as well as some styling information, is pulled from a Google Sheet (to facilitate community translation) and is automagically stored in an SQL database.

![timelnr_header_dark](https://user-images.githubusercontent.com/706110/167256943-d16e2d4d-cee9-4d71-966f-ae684251e860.png)

## Requirements

- Python 3.8
- A MySQL database
- A Docker environment

## Setup and Deployment

1. Create a MySQL database, and set the correct credentials in the config file as explained in the section below
2. Edit `start.sh` to configure your Docker environment (container name, and container port)`
3. Create a virtual environment (`python -m venv venv`) and activate it (`. venv/bin/activate`)
4. Run `start.sh` to build the Docker image and let it run on your server
5. If everything works correctly, your instance of Timelnr should be now reacheable. You can safely `deactivate` the virtual environment

## Config.py

Open `timelnr/config-sample.py` to configure Timelnr:

|                           | Description                                                | Example                            |
| ------------------------- | ---------------------------------------------------------- | ---------------------------------- |
| SECRET_KEY                | A key (byte format) you should generate yourself           | `b'MY_KEY_HERE'`                   |
| DB_HOST                   | Your database host address                                 | `http://localhost:3306`            |
| DB_NAME                   | Your database name                                         | DB_Timelnr                         |
| DB_USER                   | Your database username                                     | myUser                             |
| DB_PSW                    | Your database password                                     | myPassword                         |
| DB_TABLE_PREFIX           | The table prefix to be used. Should end with an underscore | tln\_                              |
| SPREADSHEET_ID            | The ID of the Google sheet. Can be found in the URL bar    | 1jfdwjDSe_djhJDGDHgfdsjgsdfhj_d3X0 |
| SPREADSHEET_ENTRIES_RANGE | Range covering the timeline entries information            | Entries!A3:V234                    |
| SPREADSHEET_LABELS_RANGE  | Range covering the entry labels                            | Labels!A3:D13                      |
| SPREADSHEET_LANG_RANGE    | Range covering the supported languages                     | Languages!A1:C15                   |

> **_IMPORTANT:_** Once you are done setting up the config file, rename it to `config.py`.

## Sheet structure

Here you can find a [Useful Template](https://docs.google.com/spreadsheets/d/1ZRiYTOvSCwL_b4kQMDPXzId8Y3lX_pPHKhufqx5noP0/edit?usp=sharing). Feel free to make a copy and edit to your needs.

> **_IMPORTANT:_** The sheet structure can be changed, as long as the data ranges defined in `timelnr/config.py` are correct.

The sheet should include three pages: Entries (the content of the timeline), Labels (management and styling), and Languages (list of supported languages).

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
- **COLOR**: name of the CSS class defined in the Labels page
- **SOURCE**: unused. Refers to the game that is source of that information
- **IMG**: name of the image relative to the entry. Stored in `timelnr/static/images/`
- **VID**: unused. link to a YouTube video related to the entry

> **_IMPORTANT:_** The first entry under every language column needs to be the relative language code (refer to [this list](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes)), which should also match the one defined in the Languages page.

## How to

### Pull the data from the Google Sheet

> **_NOTE:_** `importer.py` pulls data from the Sheet via the Google API. To do this it relies on the dev credentials stored in `service_account.json` (which is not included in the repo). The file can be downloaded from your developer console following the instructions below.

1. Go on the [Google Developer Console](https://console.developers.google.com)
2. Create a project, enable Drive and Sheets API, and create a Service Account
3. Copy the generated email address, and add it to the list of users having access to your Sheet
4. Generate a JSON key and download it as `service_account.json` in the project root
5. Simply run `python importer.py`

### Update the timeline entries

1. Edit the entries inside the Google Sheet
2. Run `python importer.py` to rebuild the database

### Add new languages

1. Make sure that the relative column in the Entries sheet page has the right language code
2. Make sure the Languages sheet page contains the new language. Currently the order needs to match the one in the Sheet.
3. Run `python imorter.py`. This will recreate the SQL database
4. Create a virtual environment (`python -m venv venv`) and activate it (`. venv/bin/activate`)
5. Rebuild docker image with `sh start.sh`
6. If everything works correctly, your instance of timlnr should now be reacheable, and you can now `deactivate` the virtual environment

### Change styling and labels

1. Edit the CSS files you want to change
2. Edit the labels colors from the Labels page of the sheet
3. Restart the Docker container with `docker restart timelnr`

### Notes on editing and styling

- If HTML files are changed, it's necessary to restart the Docker container (`docker restart timelnr`)
- If only CSS files are changed, it's sufficient to just refresh the web page, deleting the cache (`Ctrl`+`F5`)