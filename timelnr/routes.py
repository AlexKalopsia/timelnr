from flask import redirect, render_template, url_for
from timelnr import app, db
from timelnr.config import langs


@app.route("/timeline")
def timeline():
    return render_template('timeline.html')


@app.route("/")
def root():
    return redirect(url_for('home', curr_lang='en'))


@app.route("/<string:curr_lang>")
def home(curr_lang):
    with db.connect() as connection:

        labels = list(connection.execute(
            "SELECT `mgt_labels`.* FROM `mgt_labels`;"))

        list_labels = [
            {
                'id': id,
                'slug': slug,
                'name': name,
                'color': color
            }
            for id, slug, name, color in labels
        ]

        result = connection.execute(
            "SELECT `mgt_entries`.* FROM `mgt_entries`;")

        # Query joins entry and label if the color matches the label slug
        # result = connection.execute(
        #    "SELECT * FROM mgt_entries entry LEFT JOIN mgt_labels label ON entry.mgtColor = label.labelSlug ORDER BY mgtID")

        entries = []
        for row in result:

            label = next(
                (
                    {'slug': l[1],
                     'name': l[2],
                     'color': l[3]}
                    for l in labels
                    if l[1] == row["mgtColor"]
                ),
                {
                    'slug': '',
                    'name': '',
                    'color': ''
                }
            )

            entry = {
                'id': row['mgtID'],
                'year': row['mgtYear'],
                'event': {key: row['mgtEvent_' + key] for (key, value) in langs.items()},
                'game': row['mgtGame'],
                'source': row['mgtSource'],
                'image': row['mgtImg'],
                'label': label
            }
            entries.append(entry)
    return render_template('timeline.html', entries=entries, curr_lang=curr_lang, langs=langs, labels=list_labels)
