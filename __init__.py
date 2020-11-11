from flask import Flask

from core.collaborator_methods import collaborator_methods
from core.database import db, ma
from core.sector_methods import sector_methods


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JSON_SORT_KEYS'] = False
    db.init_app(app)
    app.db = db
    ma.init_app(app)
    app.register_blueprint(collaborator_methods)
    app.register_blueprint(sector_methods)

    return app
