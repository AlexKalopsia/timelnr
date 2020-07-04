from flask import render_template
from timelnr import app, db


@app.route("/")
@app.route("/home")
def home():
    with db.connect() as connection:
        result = connection.execute(
            "SELECT `mgt_entries`.* FROM `mgt_entries`;")
        entries = []
        for row in result:
            entry = {
                'id': row['mgtID'],
                'year': row['mgtYear'],
                'event': {
                    'en': row['mgtEvent_en'],
                    'it': row['mgtEvent_it'],
                    'fr': row['mgtEvent_fr'],
                    'de': row['mgtEvent_de'],
                    'es': row['mgtEvent_es'],
                    'ru': row['mgtEvent_ru'],
                    'nl': row['mgtEvent_nl'],
                    'br': row['mgtEvent_br'],
                    'ch': row['mgtEvent_ch'],
                    'pl': row['mgtEvent_pl'],
                    'lb': row['mgtEvent_lb']
                },
                'game': row['mgtGame'],
                'source': row['mgtSource'],
                'image': row['mgtImg'],
                'color': row['mgtColor']
            }
            entries.append(entry)
    return render_template('base.html', entries=entries)
