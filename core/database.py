from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
ma = Marshmallow()


def configure(app):
    db.init_app(app)
    app.db = db
    ma.init_app(app)


def insert(object):
    db.session.add(object)
    db.session.commit()


def update(query, json):
    query.update(json)
    db.session.commit()


def delete(object):
    db.session.delete(object)
    db.session.commit()
