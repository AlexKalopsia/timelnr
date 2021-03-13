from flask import redirect, render_template, url_for
from timelnr import app, config, db

langs = {}
with db.connect() as connection:
    response = list(connection.execute(
        "SELECT `" + config.DB_TABLE_PREFIX + "languages`.* FROM `" + config.DB_TABLE_PREFIX + "languages`;"))
    for l in response:
        langs[l[1]] = l[2]


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
            "SELECT `" + config.DB_TABLE_PREFIX + "labels`.* FROM `" + config.DB_TABLE_PREFIX + "labels`;"))

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
            "SELECT `" + config.DB_TABLE_PREFIX + "entries`.* FROM `" + config.DB_TABLE_PREFIX + "entries`;")

        entries = []
        for row in result:

            label = next(
                (
                    {'slug': l[1],
                     'name': l[2],
                     'color': l[3]}
                    for l in labels
                    if l[1] == row["Color"]
                ),
                {
                    'slug': '',
                    'name': '',
                    'color': ''
                }
            )

            entry = {
                'id': row['ID'],
                'year': row['Year'],
                'event': {key: row['Event_' + key] for (key, value) in langs.items()},
                'game': row['Game'],
                'source': row['Source'],
                'image': row['Image'],
                'video': row['Video'],
                'label': label
            }
            entries.append(entry)
    return render_template('timeline.html', entries=entries, curr_lang=curr_lang, langs=langs, labels=list_labels)
