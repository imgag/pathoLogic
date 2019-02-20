#!/usr/bin/env python3

import os
import connexion

from swagger_server import encoder
from pydblite import Base

from flask import current_app, g

def get_db():
    if 'db' not in g:
        g.db = Base(os.path.join(os.environ.get('BASE_DIR', os.getcwd()), 'pathoLogic.pdl'))
        if g.db.exists():
            g.db.open()
        else:
            g.db.create('id', 'author_email', 'created', 'last_updated', 'path_one', 'path_two', 'status', 'result')

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def main():
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'pathoLogic'})
    app.run(port=os.getenv('HTTP_PORT', 8080))
    app.teardown_appcontext(close_db)
    get_db()

if __name__ == '__main__':
    main()
