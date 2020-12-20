# Metal Gear Timeline

The MetalGearTimeline is a web app built in Pyton, Flesk and Jinja. All the data from the timeline, as well as some styling information, are stored in an SQL database that the data is pulled from.

# How to

## Add new language

- Make sure that the relative Sheet column has the right language code
- Make sure `config.py` contains the new language. Currently the order needs to match the one in the Sheet.
- Run `py imorter.py`. This will recreate the SQL database
- Rebuild docker image with `sh start.sh`

## Change styling

- Edit files
- Restart `mgt` container

### Extra info

- `importer.py` pulls data from the translation sheet via the Google API. To do this it relies on the dev credentials stored in `credentials.json` (which is not committed to the repo). The file can be re-downloaded from the dev dashboard.
