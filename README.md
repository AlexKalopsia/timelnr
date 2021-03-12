# Metal Gear Timeline

The MetalGearTimeline is a web app built in Pyton, Flesk and Jinja. All the data from the timeline, as well as some styling information, are pulled from a Google Sheet and stored in an SQL database.

## How to

### Sheet structure

All the data is pulled from a Google Sheet with the following structure:

|     |      |      |       |        |                |     | ENGLISH            | ITALIAN        | ... |
| --- | ---- | ---- | ----- | ------ | -------------- | --- | ------------------ | -------------- | --- |
| ID  | YEAR | GAME | COLOR | SOURCE | IMG            | VID | en                 | it             | ... |
| 1   | 2001 | MGS2 | mgs2  |        | mgs2header.jpg |     | Snake is born      | Nasce Snake    | ... |
| 2   |      |      |       |        |                |     | Everyone loves him | Tutti lo amano | ... |
| 3   | 2012 | MGS4 | mgs4  |        | mgs4.png       |     | Snake is dead      | Muore Snake    | ... |
| ... | ...  | ...  | ...   | ...    | ...            | ... | ...                | ...            | ... |

- ID: entry ID. Must be unique
- YEAR: the year when a specific timeline entry happened
- GAME: title of the game. Should be used only for the first entry belonging to the game
- COLOR: css class defined in 'timelnr/config.py'
- SOURCE: unused. Refers to the game that is source of that information
- IMG: name of the image relative to the entry. Stored in `timelnr/static/images/`
- VID: unused. link to a YouTube video related to the entry

IMPORTANT: The first entry under every language column needs to be the relative language code (refer to [this list](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes))

### Get your Google API credentials

1. Go on the [Google Developer Console](https://console.developers.google.com)
2. Create a project and generate a OAuth 2.0 Client ID
3. Download the credentials as JSON file
4. Store the JSON file in the project root

### Pull the data from the Google Sheet

- Simply run `py importer.py`

NOTE: `importer.py` pulls data from the translation sheet via the Google API. To do this it relies on the dev credentials stored in `credentials.json` (which is not committed to the repo). The file can be re-downloaded from the dev dashboard.

### Run the timeline

1. Setup a MySQL database, and set the credentials in 'timelnr/config.py'
2. Run `start.sh` to build the Docker image and let it run on your server

### Update the timeline entries

1. Edit the entries inside the Google Sheet
2. Run `py importer.py` to rebuild the database

### Add new language

1. Make sure that the relative Sheet column has the right language code
2. Make sure `config.py` contains the new language. Currently the order needs to match the one in the Sheet.
3. Run `py imorter.py`. This will recreate the SQL database
4. Rebuild docker image with `sh start.sh`

### Change styling

1. Edit the files you want to change
2. Restart the Docker container with `docker restart mgt`
