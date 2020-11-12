from __init__ import create_app
from database.database import db


def main():
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)


if __name__ == '__main__':
    main()
