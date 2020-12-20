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
