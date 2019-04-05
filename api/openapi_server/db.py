import os
import pickle
from flask import current_app, g

def get_db():
    if 'db' not in g:
        picklePath = os.path.join(os.getenv('BASE_DIR', os.getcwd()), 'pathoLogic.db')
        # Global dict serves as database
        if os.path.isfile(picklePath):
            g.db = pickle.load(open(picklePath, 'rb'))
        else:
            g.db = {}
            g.db['samples'] = {}
            g.db['runs'] = {}
            g.db['status_assembly'] = {}

    return g.db
