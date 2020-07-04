from timelnr import db
import datetime


class Item(db.Model):
    date = db.Column(db.DateTime, nullable=False,
                     default=datetime.utcnow())
