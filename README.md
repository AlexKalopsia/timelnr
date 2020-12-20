# Metal Gear Timeline

The MetalGearTimeline is a web app built in Pyton, Flesk and Jinja. All the data from the timeline, as well as some styling information, are stored in an SQL database that the data is pulled from.

# How to

## Add new language

* Re-export language sheet as csv UTF-8. Use `@` to separate columns.
* Import csv in `DB_MetalGearTimeline
* Add new language in `config.py`
* Rebuild docker image with `sh start.sh`

## Change styling

* Edit files
* Restart `mgt` container