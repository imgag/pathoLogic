import os
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
