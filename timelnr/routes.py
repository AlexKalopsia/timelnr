from flask import redirect, render_template, url_for
from timelnr import app, db
from timelnr.config import langs, labels, label_colors


@app.route("/timeline")
def timeline():
    return render_template('timeline.html')


@app.route("/")
def root():
    return redirect(url_for('home', curr_lang='en'))


@app.route("/<string:curr_lang>")
def home(curr_lang):
    with db.connect() as connection:
        result = connection.execute(
            "SELECT `mgt_entries`.* FROM `mgt_entries`;")
        entries = []
        for row in result:
            entry = {
                'id': row['mgtID'],
                'year': row['mgtYear'],
                'event': {key: row['mgtEvent_' + key] for (key, value) in langs.items()},
                'game': row['mgtGame'],
                'source': row['mgtSource'],
                'image': row['mgtImg'],
                'label': {
                    'slug': row['mgtColor'],
                    'color': label_colors.get(row['mgtColor']),
                    'name': row['mgtGame']
                }
            }
            entries.append(entry)
    return render_template('timeline.html', entries=entries, curr_lang=curr_lang, langs=langs, labels=labels)
